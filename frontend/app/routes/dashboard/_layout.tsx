import { Outlet } from "react-router";
import { DashboardLayout } from "~/features/dashboard/components/layout";

export default function DashboardLayoutRoute() {
  return (
    <DashboardLayout>
      <Outlet />
    </DashboardLayout>
  );
}