export const workflowSteps = [
  {
    id: 1,
    name: 'Create User Accounts',
    description: 'Set up accounts in AD, Email, and internal systems',
    agentId: 'data-retrieval',
    estimatedTime: 3000,
  },
  {
    id: 2,
    name: 'Assign Buddy',
    description: 'Match new employee with appropriate mentor based on department',
    agentId: 'decision-making',
    estimatedTime: 2500,
  },
  {
    id: 3,
    name: 'Schedule Meetings',
    description: 'Book orientation, team intro, and 1:1 meetings',
    agentId: 'action-execution',
    estimatedTime: 3000,
  },
  {
    id: 4,
    name: 'Send Welcome Email',
    description: 'Send personalized welcome package with credentials',
    agentId: 'action-execution',
    estimatedTime: 2000,
    canFail: true, // This step can fail to demonstrate error handling
  },
  {
    id: 5,
    name: 'Verify & Audit',
    description: 'Confirm all steps completed and log for compliance',
    agentId: 'verification',
    estimatedTime: 2500,
  },
];

export const workflowConfig = {
  name: 'Employee Onboarding',
  description: 'Automated onboarding workflow for new employees',
  steps: workflowSteps,
  maxRetries: 2,
};
