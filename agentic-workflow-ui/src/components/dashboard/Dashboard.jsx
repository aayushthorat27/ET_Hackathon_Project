import { WorkflowStatusCard } from './WorkflowStatusCard';
import { ActiveAgentsCard } from './ActiveAgentsCard';
import { ActivityTimeline } from './ActivityTimeline';
import { workflowSteps } from '../../data/workflows';

export function Dashboard({ workflowState }) {
  const { status, currentStep, logs, activeAgent } = workflowState;

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-gray-900">Dashboard</h2>
        <p className="text-gray-600">Monitor your autonomous workflow execution</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 space-y-6">
          <WorkflowStatusCard
            status={status}
            currentStep={currentStep}
            totalSteps={workflowSteps.length}
          />
          <ActivityTimeline logs={logs} />
        </div>
        <div>
          <ActiveAgentsCard activeAgent={activeAgent} />
        </div>
      </div>
    </div>
  );
}
