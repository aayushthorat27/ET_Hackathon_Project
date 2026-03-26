import { Card, CardHeader, CardTitle, CardContent, Badge, Button } from '../ui';
import { LogEntry } from './LogEntry';
import { ClipboardList, Download, Filter, Trash2 } from 'lucide-react';
import { useState } from 'react';

export function AuditTrailPanel({ logs = [], onClear }) {
  const [filter, setFilter] = useState('all');

  const filteredLogs = logs.filter((log) => {
    if (filter === 'all') return true;
    return log.type === filter;
  });

  const counts = {
    all: logs.length,
    info: logs.filter((l) => l.type === 'info').length,
    success: logs.filter((l) => l.type === 'success').length,
    warning: logs.filter((l) => l.type === 'warning').length,
    error: logs.filter((l) => l.type === 'error').length,
  };

  const exportLogs = () => {
    const data = JSON.stringify(logs, null, 2);
    const blob = new Blob([data], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `audit-log-${new Date().toISOString().split('T')[0]}.json`;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-gray-900">Audit Trail</h2>
          <p className="text-gray-600">Complete log of all workflow actions and decisions</p>
        </div>
        <div className="flex gap-2">
          <Button variant="outline" size="sm" onClick={exportLogs} disabled={logs.length === 0}>
            <Download className="w-4 h-4" />
            Export
          </Button>
          <Button variant="outline" size="sm" onClick={onClear} disabled={logs.length === 0}>
            <Trash2 className="w-4 h-4" />
            Clear
          </Button>
        </div>
      </div>

      {/* Filter Tabs */}
      <div className="flex gap-2 flex-wrap">
        {['all', 'info', 'success', 'warning', 'error'].map((type) => (
          <button
            key={type}
            onClick={() => setFilter(type)}
            className={`px-3 py-1.5 rounded-full text-sm font-medium transition-colors ${
              filter === type
                ? 'bg-primary text-white'
                : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
            }`}
          >
            {type.charAt(0).toUpperCase() + type.slice(1)} ({counts[type]})
          </button>
        ))}
      </div>

      {/* Log List */}
      {filteredLogs.length === 0 ? (
        <Card>
          <CardContent className="py-12 text-center">
            <ClipboardList className="w-12 h-12 mx-auto text-gray-300 mb-4" />
            <p className="text-gray-500">No audit logs to display</p>
            <p className="text-sm text-gray-400">Start a workflow to generate logs</p>
          </CardContent>
        </Card>
      ) : (
        <div className="space-y-3">
          {filteredLogs.map((log, index) => (
            <LogEntry key={`${log.timestamp}-${index}`} log={log} index={index} />
          ))}
        </div>
      )}

      {/* Summary Stats */}
      {logs.length > 0 && (
        <Card>
          <CardContent className="py-4">
            <div className="grid grid-cols-2 md:grid-cols-5 gap-4 text-center">
              <div>
                <p className="text-2xl font-bold text-gray-900">{counts.all}</p>
                <p className="text-xs text-gray-500">Total Events</p>
              </div>
              <div>
                <p className="text-2xl font-bold text-blue-600">{counts.info}</p>
                <p className="text-xs text-gray-500">Info</p>
              </div>
              <div>
                <p className="text-2xl font-bold text-green-600">{counts.success}</p>
                <p className="text-xs text-gray-500">Success</p>
              </div>
              <div>
                <p className="text-2xl font-bold text-yellow-600">{counts.warning}</p>
                <p className="text-xs text-gray-500">Warnings</p>
              </div>
              <div>
                <p className="text-2xl font-bold text-red-600">{counts.error}</p>
                <p className="text-xs text-gray-500">Errors</p>
              </div>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
