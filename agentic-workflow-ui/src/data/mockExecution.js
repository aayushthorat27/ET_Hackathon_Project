import { workflowSteps } from './workflows';
import { getAgentById } from './agents';

export const generateStepLogs = (step, status, retryCount = 0) => {
  const agent = getAgentById(step.agentId);
  const timestamp = new Date().toISOString();

  const baseLog = {
    timestamp,
    stepId: step.id,
    stepName: step.name,
    agentId: step.agentId,
    agentName: agent.name,
  };

  switch (status) {
    case 'started':
      return {
        ...baseLog,
        type: 'info',
        message: `Started: ${step.name}`,
        reasoning: `Orchestrator delegated task to ${agent.name}. ${step.description}`,
      };

    case 'completed':
      return {
        ...baseLog,
        type: 'success',
        message: `Completed: ${step.name}`,
        reasoning: getCompletionReasoning(step),
      };

    case 'failed':
      return {
        ...baseLog,
        type: 'error',
        message: `Failed: ${step.name} (Attempt ${retryCount + 1})`,
        reasoning: getFailureReasoning(step),
      };

    case 'retry':
      return {
        ...baseLog,
        type: 'warning',
        message: `Retrying: ${step.name} (Attempt ${retryCount + 1})`,
        reasoning: `Previous attempt failed. Initiating retry with exponential backoff.`,
      };

    case 'escalated':
      return {
        ...baseLog,
        type: 'error',
        message: `Escalated: ${step.name} - Requires human intervention`,
        reasoning: `Maximum retry attempts exceeded. Escalating to system administrator for manual resolution.`,
      };

    default:
      return baseLog;
  }
};

const getCompletionReasoning = (step) => {
  const reasonings = {
    1: 'Successfully created accounts in Active Directory, Microsoft 365, and internal HR system. All credentials generated and stored securely.',
    2: 'Analyzed department structure and availability. Selected Sarah Chen as buddy based on role alignment, experience, and current mentee capacity.',
    3: 'Scheduled 5 meetings: Day 1 orientation (9 AM), Team intro (2 PM), HR onboarding (Day 2 10 AM), IT setup (Day 2 2 PM), Manager 1:1 (Day 3 11 AM).',
    4: 'Welcome email sent successfully with login credentials, first-week schedule, company handbook link, and buddy introduction.',
    5: 'All onboarding steps verified. Audit log generated: 5/5 tasks completed. Compliance check passed. Record created in HR system.',
  };
  return reasonings[step.id] || 'Task completed successfully.';
};

const getFailureReasoning = (step) => {
  const failures = {
    4: 'SMTP server connection timeout. Unable to send email via primary mail server. Error code: CONN_TIMEOUT_587.',
  };
  return failures[step.id] || 'An unexpected error occurred during execution.';
};

export const simulateWorkflowExecution = async (employeeData, onUpdate) => {
  const logs = [];
  let failedStep4 = false;
  let retryCount = 0;

  // Initial orchestrator log
  logs.push({
    timestamp: new Date().toISOString(),
    type: 'info',
    agentId: 'orchestrator',
    agentName: 'Orchestrator Agent',
    message: `Workflow initiated for ${employeeData.name}`,
    reasoning: `Received onboarding request. Analyzing workflow steps and preparing agent delegation sequence.`,
  });
  onUpdate({ logs: [...logs], currentStep: 0, status: 'running' });

  await delay(1500);

  for (let i = 0; i < workflowSteps.length; i++) {
    const step = workflowSteps[i];

    // Start step
    logs.push(generateStepLogs(step, 'started'));
    onUpdate({ logs: [...logs], currentStep: i + 1, status: 'running', activeAgent: step.agentId });

    await delay(step.estimatedTime);

    // Simulate failure on step 4 (first attempt)
    if (step.canFail && !failedStep4) {
      failedStep4 = true;
      retryCount = 0;

      // First failure
      logs.push(generateStepLogs(step, 'failed', retryCount));
      onUpdate({ logs: [...logs], currentStep: i + 1, status: 'error', activeAgent: step.agentId });

      await delay(1500);

      // Retry loop
      while (retryCount < 2) {
        retryCount++;
        logs.push(generateStepLogs(step, 'retry', retryCount));
        onUpdate({ logs: [...logs], currentStep: i + 1, status: 'retrying', activeAgent: step.agentId });

        await delay(2000);

        if (retryCount === 2) {
          // Second retry succeeds
          logs.push(generateStepLogs(step, 'completed'));
          onUpdate({ logs: [...logs], currentStep: i + 1, status: 'running', activeAgent: step.agentId });
          break;
        } else {
          // First retry also fails
          logs.push(generateStepLogs(step, 'failed', retryCount));
          onUpdate({ logs: [...logs], currentStep: i + 1, status: 'error', activeAgent: step.agentId });
          await delay(1000);
        }
      }
    } else {
      // Normal completion
      logs.push(generateStepLogs(step, 'completed'));
      onUpdate({ logs: [...logs], currentStep: i + 1, status: 'running', activeAgent: step.agentId });
    }

    await delay(500);
  }

  // Final orchestrator log
  logs.push({
    timestamp: new Date().toISOString(),
    type: 'success',
    agentId: 'orchestrator',
    agentName: 'Orchestrator Agent',
    message: 'Workflow completed successfully',
    reasoning: `All 5 onboarding steps completed for ${employeeData.name}. Total time: ${calculateTotalTime(logs)}. 1 error recovered via retry mechanism.`,
  });
  onUpdate({ logs: [...logs], currentStep: workflowSteps.length, status: 'completed', activeAgent: null });
};

const delay = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

const calculateTotalTime = (logs) => {
  if (logs.length < 2) return '0s';
  const start = new Date(logs[0].timestamp);
  const end = new Date(logs[logs.length - 1].timestamp);
  const diffMs = end - start;
  const seconds = Math.floor(diffMs / 1000);
  return `${seconds}s`;
};
