import { useState } from 'react';
import { Layout } from './components/layout';
import { Dashboard } from './components/dashboard';
import { WorkflowInputPanel, WorkflowStepper, AgentExecutionView } from './components/workflow';
import { AuditTrailPanel } from './components/audit';
import { useWorkflow } from './hooks';
import './index.css';

function App() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const workflow = useWorkflow();

  const renderContent = () => {
    switch (activeTab) {
      case 'dashboard':
        return <Dashboard workflowState={workflow} />;

      case 'workflows':
        return (
          <div className="space-y-6">
            <div>
              <h2 className="text-2xl font-bold text-gray-900">Workflows</h2>
              <p className="text-gray-600">
                Execute and monitor autonomous enterprise workflows
              </p>
            </div>
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              <div className="lg:col-span-1">
                <WorkflowInputPanel
                  onStartWorkflow={workflow.startWorkflow}
                  isRunning={workflow.isRunning}
                />
              </div>
              <div className="lg:col-span-1">
                <WorkflowStepper
                  currentStep={workflow.currentStep}
                  status={workflow.status}
                  activeAgent={workflow.activeAgent}
                />
              </div>
              <div className="lg:col-span-1">
                <AgentExecutionView
                  activeAgent={workflow.activeAgent}
                  logs={workflow.logs}
                />
              </div>
            </div>
          </div>
        );

      case 'audit':
        return (
          <AuditTrailPanel logs={workflow.logs} onClear={workflow.clearLogs} />
        );

      case 'settings':
        return (
          <div className="space-y-6">
            <div>
              <h2 className="text-2xl font-bold text-gray-900">Settings</h2>
              <p className="text-gray-600">Configure your workflow system</p>
            </div>
            <div className="bg-white rounded-xl border border-gray-100 p-6">
              <p className="text-gray-500 text-center py-12">
                Settings panel coming soon...
              </p>
            </div>
          </div>
        );

      default:
        return <Dashboard workflowState={workflow} />;
    }
  };

  return (
    <Layout activeTab={activeTab} onTabChange={setActiveTab}>
      {renderContent()}
    </Layout>
  );
}

export default App;
