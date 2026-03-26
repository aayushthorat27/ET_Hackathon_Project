import { Card, CardHeader, CardTitle, CardContent } from '../ui';
import { StatusIndicator } from '../ui';
import { CheckCircle, Clock, AlertTriangle, XCircle } from 'lucide-react';

const statusConfig = {
  idle: {
    icon: Clock,
    label: 'Ready to Start',
    description: 'No active workflows',
    color: 'text-gray-500',
    bg: 'bg-gray-50',
  },
  running: {
    icon: Clock,
    label: 'In Progress',
    description: 'Workflow executing',
    color: 'text-primary',
    bg: 'bg-primary/5',
  },
  completed: {
    icon: CheckCircle,
    label: 'Completed',
    description: 'Workflow finished successfully',
    color: 'text-green-600',
    bg: 'bg-green-50',
  },
  error: {
    icon: XCircle,
    label: 'Error',
    description: 'Error encountered',
    color: 'text-red-600',
    bg: 'bg-red-50',
  },
  retrying: {
    icon: AlertTriangle,
    label: 'Retrying',
    description: 'Attempting recovery',
    color: 'text-tertiary',
    bg: 'bg-tertiary/10',
  },
};

export function WorkflowStatusCard({ status = 'idle', currentStep, totalSteps }) {
  const config = statusConfig[status] || statusConfig.idle;
  const Icon = config.icon;

  return (
    <Card>
      <CardHeader>
        <CardTitle>Workflow Status</CardTitle>
      </CardHeader>
      <CardContent>
        <div className={`rounded-lg p-4 ${config.bg}`}>
          <div className="flex items-center gap-3">
            <div className={`p-2 rounded-full ${config.bg}`}>
              <Icon className={`w-6 h-6 ${config.color}`} />
            </div>
            <div>
              <p className={`font-semibold ${config.color}`}>{config.label}</p>
              <p className="text-sm text-gray-600">{config.description}</p>
            </div>
          </div>
          {status !== 'idle' && (
            <div className="mt-4">
              <div className="flex justify-between text-sm mb-1">
                <span className="text-gray-600">Progress</span>
                <span className="font-medium">
                  {currentStep}/{totalSteps} steps
                </span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div
                  className="bg-primary rounded-full h-2 transition-all duration-500"
                  style={{ width: `${(currentStep / totalSteps) * 100}%` }}
                />
              </div>
            </div>
          )}
        </div>
      </CardContent>
    </Card>
  );
}
