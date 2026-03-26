import { Card, CardHeader, CardTitle, CardContent, StatusIndicator } from '../ui';
import { agents } from '../../data/agents';

export function ActiveAgentsCard({ activeAgent }) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Active Agents</CardTitle>
      </CardHeader>
      <CardContent className="p-0">
        <div className="divide-y divide-gray-100">
          {agents.map((agent) => {
            const Icon = agent.icon;
            const isActive = activeAgent === agent.id;
            const status = isActive ? 'active' : 'idle';

            return (
              <div
                key={agent.id}
                className={`px-6 py-4 flex items-center gap-4 transition-colors ${
                  isActive ? 'bg-primary/5' : ''
                }`}
              >
                <div
                  className={`w-10 h-10 rounded-lg flex items-center justify-center ${
                    isActive ? 'bg-primary text-white' : 'bg-gray-100 text-gray-500'
                  }`}
                >
                  <Icon className="w-5 h-5" />
                </div>
                <div className="flex-1 min-w-0">
                  <p className={`font-medium truncate ${isActive ? 'text-primary' : 'text-gray-900'}`}>
                    {agent.name}
                  </p>
                  <p className="text-sm text-gray-500 truncate">{agent.role}</p>
                </div>
                <StatusIndicator status={status} showLabel={false} />
              </div>
            );
          })}
        </div>
      </CardContent>
    </Card>
  );
}
