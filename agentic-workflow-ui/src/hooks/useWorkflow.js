import { useState, useCallback } from 'react';
import { simulateWorkflowExecution } from '../data/mockExecution';

const initialState = {
  status: 'idle', // idle, running, error, retrying, completed
  currentStep: 0,
  logs: [],
  activeAgent: null,
  employeeData: null,
};

export function useWorkflow() {
  const [state, setState] = useState(initialState);

  const startWorkflow = useCallback(async (employeeData) => {
    setState({
      ...initialState,
      status: 'running',
      employeeData,
    });

    await simulateWorkflowExecution(employeeData, (update) => {
      setState((prev) => ({
        ...prev,
        ...update,
      }));
    });
  }, []);

  const resetWorkflow = useCallback(() => {
    setState(initialState);
  }, []);

  const clearLogs = useCallback(() => {
    setState((prev) => ({
      ...prev,
      logs: [],
    }));
  }, []);

  const isRunning = state.status === 'running' || state.status === 'retrying';

  return {
    ...state,
    isRunning,
    startWorkflow,
    resetWorkflow,
    clearLogs,
  };
}
