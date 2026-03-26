import { Card, CardHeader, CardTitle, CardContent, Badge } from '../ui';
import { Clock } from 'lucide-react';

const typeStyles = {
  info: { variant: 'info', icon: '📋' },
  success: { variant: 'success', icon: '✅' },
  warning: { variant: 'warning', icon: '⚠️' },
  error: { variant: 'error', icon: '❌' },
};

export function ActivityTimeline({ logs = [] }) {
  const recentLogs = logs.slice(-10).reverse();

  return (
    <Card className="h-full">
      <CardHeader>
        <div className="flex items-center justify-between">
          <CardTitle>Activity Timeline</CardTitle>
          <Badge variant="default">{logs.length} events</Badge>
        </div>
      </CardHeader>
      <CardContent className="p-0 max-h-96 overflow-y-auto">
        {recentLogs.length === 0 ? (
          <div className="p-6 text-center text-gray-500">
            <Clock className="w-8 h-8 mx-auto mb-2 opacity-50" />
            <p>No activity yet</p>
            <p className="text-sm">Start a workflow to see events</p>
          </div>
        ) : (
          <div className="divide-y divide-gray-100">
            {recentLogs.map((log, index) => {
              const style = typeStyles[log.type] || typeStyles.info;
              const time = new Date(log.timestamp).toLocaleTimeString();

              return (
                <div
                  key={`${log.timestamp}-${index}`}
                  className="px-6 py-3 animate-fade-in-up"
                  style={{ animationDelay: `${index * 50}ms` }}
                >
                  <div className="flex items-start gap-3">
                    <span className="text-lg">{style.icon}</span>
                    <div className="flex-1 min-w-0">
                      <p className="font-medium text-gray-900 text-sm">{log.message}</p>
                      <p className="text-xs text-gray-500 mt-0.5">{log.agentName}</p>
                    </div>
                    <span className="text-xs text-gray-400 whitespace-nowrap">{time}</span>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </CardContent>
    </Card>
  );
}
