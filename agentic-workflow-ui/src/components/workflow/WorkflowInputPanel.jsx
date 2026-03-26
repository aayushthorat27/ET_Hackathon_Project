import { useState } from 'react';
import { Card, CardHeader, CardTitle, CardContent, Button } from '../ui';
import { User, Mail, Building, Calendar, Play } from 'lucide-react';

export function WorkflowInputPanel({ onStartWorkflow, isRunning }) {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    department: '',
    startDate: '',
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    if (formData.name && formData.email && formData.department) {
      onStartWorkflow(formData);
    }
  };

  const handleChange = (field) => (e) => {
    setFormData((prev) => ({ ...prev, [field]: e.target.value }));
  };

  const isValid = formData.name && formData.email && formData.department;

  return (
    <Card>
      <CardHeader>
        <CardTitle>Employee Onboarding</CardTitle>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              <User className="w-4 h-4 inline mr-1" />
              Employee Name
            </label>
            <input
              type="text"
              value={formData.name}
              onChange={handleChange('name')}
              placeholder="John Doe"
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary/50 focus:border-primary"
              disabled={isRunning}
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              <Mail className="w-4 h-4 inline mr-1" />
              Email
            </label>
            <input
              type="email"
              value={formData.email}
              onChange={handleChange('email')}
              placeholder="john.doe@company.com"
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary/50 focus:border-primary"
              disabled={isRunning}
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              <Building className="w-4 h-4 inline mr-1" />
              Department
            </label>
            <select
              value={formData.department}
              onChange={handleChange('department')}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary/50 focus:border-primary"
              disabled={isRunning}
            >
              <option value="">Select department</option>
              <option value="engineering">Engineering</option>
              <option value="marketing">Marketing</option>
              <option value="sales">Sales</option>
              <option value="hr">Human Resources</option>
              <option value="finance">Finance</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              <Calendar className="w-4 h-4 inline mr-1" />
              Start Date
            </label>
            <input
              type="date"
              value={formData.startDate}
              onChange={handleChange('startDate')}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary/50 focus:border-primary"
              disabled={isRunning}
            />
          </div>

          <Button
            type="submit"
            className="w-full"
            disabled={!isValid || isRunning}
            loading={isRunning}
          >
            <Play className="w-4 h-4" />
            {isRunning ? 'Processing...' : 'Start Onboarding'}
          </Button>
        </form>
      </CardContent>
    </Card>
  );
}
