const statusStyles = {
  idle: {
    dot: 'bg-gray-400',
    ring: '',
    text: 'text-gray-500',
    label: 'Idle',
  },
  active: {
    dot: 'bg-primary',
    ring: 'animate-pulse-ring',
    text: 'text-primary',
    label: 'Active',
  },
  completed: {
    dot: 'bg-green-500',
    ring: '',
    text: 'text-green-600',
    label: 'Completed',
  },
  error: {
    dot: 'bg-red-500',
    ring: '',
    text: 'text-red-600',
    label: 'Error',
  },
  pending: {
    dot: 'bg-tertiary',
    ring: '',
    text: 'text-tertiary',
    label: 'Pending',
  },
};

export function StatusIndicator({ status = 'idle', showLabel = true, size = 'md' }) {
  const styles = statusStyles[status] || statusStyles.idle;
  const dotSize = size === 'sm' ? 'w-2 h-2' : 'w-3 h-3';

  return (
    <div className="flex items-center gap-2">
      <div className="relative">
        <span className={`block ${dotSize} rounded-full ${styles.dot}`} />
        {styles.ring && (
          <span
            className={`absolute inset-0 ${dotSize} rounded-full ${styles.dot} opacity-50 ${styles.ring}`}
          />
        )}
      </div>
      {showLabel && (
        <span className={`text-sm font-medium ${styles.text}`}>{styles.label}</span>
      )}
    </div>
  );
}
