import { Card, CardHeader, CardTitle, CardContent, Badge } from '../ui';
import { workflowSteps } from '../../data/workflows';
import { getAgentById } from '../../data/agents';
import { Check, Circle, Loader2, AlertCircle, RotateCcw } from 'lucide-react';

const stepStatusConfig = {
  pending: {
    icon: Circle,
    color: 'text-gray-400',
    bg: 'bg-gray-100',
    line: 'bg-gray-200',
  },
  active: {
    icon: Loader2,
    color: 'text-primary',
    bg: 'bg-primary',
    line: 'bg-primary',
    animate: true,
  },
  completed: {
    icon: Check,
    color: 'text-white',
    bg: 'bg-green-500',
    line: 'bg-green-500',
  },
  error: {
    icon: AlertCircle,
    color: 'text-white',
    bg: 'bg-red-500',
    line: 'bg-red-500',
  },
  retrying: {
    icon: RotateCcw,
    color: 'text-white',
    bg: 'bg-tertiary',
    line: 'bg-tertiary',
    animate: true,
  },
};

export function WorkflowStepper({ currentStep, status, activeAgent }) {
  const getStepStatus = (stepIndex) => {
    const stepNumber = stepIndex + 1;
    if (stepNumber < currentStep) return 'completed';
    if (stepNumber === currentStep) {
      if (status === 'error') return 'error';
      if (status === 'retrying') return 'retrying';
      return 'active';
    }
    return 'pending';
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle>Workflow Progress</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-0">
          {workflowSteps.map((step, index) => {
            const stepStatus = getStepStatus(index);
            const config = stepStatusConfig[stepStatus];
            const Icon = config.icon;
            const agent = getAgentById(step.agentId);
            const AgentIcon = agent.icon;
            const isLast = index === workflowSteps.length - 1;

            return (
              <div key={step.id} className="flex gap-4">
                {/* Timeline */}
                <div className="flex flex-col items-center">
                  <div
                    className={`w-10 h-10 rounded-full flex items-center justify-center ${config.bg} transition-all duration-300`}
                  >
                    <Icon
                      className={`w-5 h-5 ${config.color} ${config.animate ? 'animate-spin' : ''}`}
                    />
                  </div>
                  {!isLast && (
                    <div
                      className={`w-0.5 h-16 ${config.line} transition-all duration-300`}
                    />
                  )}
                </div>

                {/* Content */}
                <div className={`flex-1 pb-6 ${isLast ? 'pb-0' : ''}`}>
                  <div className="flex items-center gap-2 mb-1">
                    <h4
                      className={`font-medium ${
                        stepStatus === 'pending' ? 'text-gray-400' : 'text-gray-900'
                      }`}
                    >
                      {step.name}
                    </h4>
                    {stepStatus === 'active' && (
                      <Badge variant="primary">In Progress</Badge>
                    )}
                    {stepStatus === 'error' && <Badge variant="error">Error</Badge>}
                    {stepStatus === 'retrying' && <Badge variant="warning">Retrying</Badge>}
                    {stepStatus === 'completed' && <Badge variant="success">Done</Badge>}
                  </div>
                  <p className="text-sm text-gray-500 mb-2">{step.description}</p>
                  <div className="flex items-center gap-2 text-xs text-gray-400">
                    <AgentIcon className="w-3 h-3" />
                    <span>{agent.name}</span>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </CardContent>
    </Card>
  );
}
