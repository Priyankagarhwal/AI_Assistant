import { Routes, Route } from "react-router-dom";

import MainLayout from "../layouts/MainLayout";

import Dashboard from "../pages/Dashboard";
import Workspaces from "../pages/Workspaces";
import Upload from "../pages/Upload";
import Chat from "../pages/Chat";
import History from "../pages/History";
import Summary from "../pages/Summary";

export default function AppRoutes() {
  return (
    <Routes>
      <Route
        path="/"
        element={
          <MainLayout>
            <Dashboard />
          </MainLayout>
        }
      />

      <Route
        path="/workspaces"
        element={
          <MainLayout>
            <Workspaces />
          </MainLayout>
        }
      />

      <Route
        path="/upload"
        element={
          <MainLayout>
            <Upload />
          </MainLayout>
        }
      />

      <Route
        path="/chat"
        element={
          <MainLayout>
            <Chat />
          </MainLayout>
        }
      />

      <Route
        path="/history"
        element={
          <MainLayout>
            <History />
          </MainLayout>
        }
      />

      <Route
        path="/summary"
        element={
          <MainLayout>
            <Summary />
          </MainLayout>
        }
      />
    </Routes>
  );
}