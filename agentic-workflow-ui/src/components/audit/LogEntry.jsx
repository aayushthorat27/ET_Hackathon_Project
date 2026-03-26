import { Badge } from '../ui';
import { ChevronDown, ChevronUp } from 'lucide-react';
import { useState } from 'react';

const typeConfig = {
  info: {
    bg: 'bg-blue-50',
    border: 'border-blue-200',
    icon: '📋',
    badge: 'info',
  },
  success: {
    bg: 'bg-green-50',
    border: 'border-green-200',
    icon: '✅',
    badge: 'success',
  },
  warning: {
    bg: 'bg-yellow-50',
    border: 'border-yellow-200',
    icon: '⚠️',
    badge: 'warning',
  },
  error: {
    bg: 'bg-red-50',
    border: 'border-red-200',
    icon: '❌',
    badge: 'error',
  },
};

export function LogEntry({ log, index }) {
  const [expanded, setExpanded] = useState(false);
  const config = typeConfig[log.type] || typeConfig.info;
  const time = new Date(log.timestamp).toLocaleTimeString();
  const date = new Date(log.timestamp).toLocaleDateString();

  return (
    <div
      className={`rounded-lg border ${config.border} ${config.bg} overflow-hidden animate-fade-in-up`}
      style={{ animationDelay: `${index * 30}ms` }}
    >
      <button
        onClick={() => setExpanded(!expanded)}
        className="w-full p-4 flex items-start gap-3 text-left hover:opacity-90 transition-opacity"
      >
        <span className="text-xl">{config.icon}</span>
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 mb-1">
            <Badge variant={config.badge}>{log.type.toUpperCase()}</Badge>
            <span className="text-xs text-gray-500">
              {date} {time}
            </span>
          </div>
          <p className="font-medium text-gray-900">{log.message}</p>
          <p className="text-sm text-gray-600 mt-0.5">{log.agentName}</p>
        </div>
        {log.reasoning && (
          <div className="flex-shrink-0">
            {expanded ? (
              <ChevronUp className="w-5 h-5 text-gray-400" />
            ) : (
              <ChevronDown className="w-5 h-5 text-gray-400" />
            )}
          </div>
        )}
      </button>
      {expanded && log.reasoning && (
        <div className="px-4 pb-4 pt-0">
          <div className="ml-9 p-3 bg-white/60 rounded-lg border border-gray-200">
            <p className="text-xs font-medium text-gray-500 mb-1">Agent Reasoning:</p>
            <p className="text-sm text-gray-700">{log.reasoning}</p>
          </div>
        </div>
      )}
    </div>
  );
}
