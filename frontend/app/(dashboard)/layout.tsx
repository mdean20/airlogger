import { Navigation } from "@/components/layout/Navigation";

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <>
      <Navigation />
      <main className="min-vh-100-navbar">
        {children}
      </main>
    </>
  );
}