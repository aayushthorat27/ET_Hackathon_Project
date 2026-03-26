import {
  Brain,
  Database,
  Lightbulb,
  Zap,
  Shield,
} from 'lucide-react';

export const agents = [
  {
    id: 'orchestrator',
    name: 'Orchestrator Agent',
    role: 'Controls workflow execution and coordinates other agents',
    icon: Brain,
    color: 'primary',
  },
  {
    id: 'data-retrieval',
    name: 'Data Retrieval Agent',
    role: 'Fetches and validates data from enterprise systems',
    icon: Database,
    color: 'blue',
  },
  {
    id: 'decision-making',
    name: 'Decision-Making Agent',
    role: 'Analyzes data and makes intelligent decisions',
    icon: Lightbulb,
    color: 'tertiary',
  },
  {
    id: 'action-execution',
    name: 'Action Execution Agent',
    role: 'Performs actions in external systems',
    icon: Zap,
    color: 'green',
  },
  {
    id: 'verification',
    name: 'Verification Agent',
    role: 'Audits actions and ensures compliance',
    icon: Shield,
    color: 'purple',
  },
];

export const getAgentById = (id) => agents.find((a) => a.id === id);
