import { Card, CardHeader, CardTitle, CardContent, Badge } from '../ui';
import { getAgentById, agents } from '../../data/agents';
import { Brain, ChevronDown, ChevronUp } from 'lucide-react';
import { useState } from 'react';

export function AgentExecutionView({ activeAgent, logs }) {
  const [expandedLogs, setExpandedLogs] = useState({});

  const toggleLog = (index) => {
    setExpandedLogs((prev) => ({ ...prev, [index]: !prev[index] }));
  };

  const agent = activeAgent ? getAgentById(activeAgent) : null;
  const recentLogs = logs.slice(-5).reverse();

  return (
    <Card className="h-full">
      <CardHeader>
        <CardTitle>Agent Execution</CardTitle>
      </CardHeader>
      <CardContent>
        {/* Active Agent Display */}
        {agent ? (
          <div className="mb-6 p-4 bg-primary/5 rounded-lg border border-primary/20">
            <div className="flex items-center gap-3">
              <div className="relative">
                <div className="w-12 h-12 bg-primary rounded-xl flex items-center justify-center">
                  <agent.icon className="w-6 h-6 text-white" />
                </div>
                <span className="absolute -bottom-1 -right-1 w-4 h-4 bg-green-500 rounded-full border-2 border-white animate-pulse" />
              </div>
              <div>
                <p className="font-semibold text-gray-900">{agent.name}</p>
                <p className="text-sm text-gray-600">{agent.role}</p>
              </div>
            </div>
          </div>
        ) : (
          <div className="mb-6 p-4 bg-gray-50 rounded-lg border border-gray-200">
            <div className="flex items-center gap-3">
              <div className="w-12 h-12 bg-gray-200 rounded-xl flex items-center justify-center">
                <Brain className="w-6 h-6 text-gray-400" />
              </div>
              <div>
                <p className="font-semibold text-gray-500">No Active Agent</p>
                <p className="text-sm text-gray-400">Waiting for workflow to start</p>
              </div>
            </div>
          </div>
        )}

        {/* Decision/Reasoning Log */}
        <div>
          <h4 className="text-sm font-medium text-gray-700 mb-3">Recent Decisions</h4>
          {recentLogs.length === 0 ? (
            <p className="text-sm text-gray-400 text-center py-4">
              No decisions yet
            </p>
          ) : (
            <div className="space-y-2">
              {recentLogs.map((log, index) => (
                <div
                  key={`${log.timestamp}-${index}`}
                  className="border border-gray-100 rounded-lg overflow-hidden animate-fade-in-up"
                >
                  <button
                    onClick={() => toggleLog(index)}
                    className="w-full px-4 py-2 flex items-center justify-between hover:bg-gray-50 text-left"
                  >
                    <div className="flex items-center gap-2">
                      <Badge
                        variant={
                          log.type === 'success'
                            ? 'success'
                            : log.type === 'error'
                            ? 'error'
                            : log.type === 'warning'
                            ? 'warning'
                            : 'info'
                        }
                      >
                        {log.agentName?.split(' ')[0] || 'System'}
                      </Badge>
                      <span className="text-sm text-gray-700 truncate max-w-xs">
                        {log.message}
                      </span>
                    </div>
                    {expandedLogs[index] ? (
                      <ChevronUp className="w-4 h-4 text-gray-400" />
                    ) : (
                      <ChevronDown className="w-4 h-4 text-gray-400" />
                    )}
                  </button>
                  {expandedLogs[index] && log.reasoning && (
                    <div className="px-4 py-3 bg-gray-50 border-t border-gray-100">
                      <p className="text-xs text-gray-500 mb-1">Reasoning:</p>
                      <p className="text-sm text-gray-700">{log.reasoning}</p>
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>
      </CardContent>
    </Card>
  );
}
