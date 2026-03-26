import { Header } from './Header';
import { Sidebar } from './Sidebar';

export function Layout({ children, activeTab, onTabChange }) {
  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      <div className="flex">
        <Sidebar activeTab={activeTab} onTabChange={onTabChange} />
        <main className="flex-1 p-6">{children}</main>
      </div>
    </div>
  );
}
