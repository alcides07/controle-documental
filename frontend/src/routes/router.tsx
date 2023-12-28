import React from "react";
import ReactDOM from "react-dom/client";
import { createBrowserRouter } from "react-router-dom";
import HomePage from "../features/HomePage";
import Dashboard from "../features/Dashboard";
import Login from "../features/Auth/Login";
import Register from "../features/Auth/Register";
import PageNotFound from "../features/PageNotFound";
import App from "../App";
import TableComponent from "../components/Table";

export const router = createBrowserRouter([
	{
		path: "/",
		element: <App />,
		errorElement: <PageNotFound />,
		children: [
			{
				path: "/",
				element: <HomePage />,
			},
			{
				path: "/login",
				element: <Login />,
			},
			{
				path: "/register",
				element: <Register />,
			},
			{
				path: "/dashboard",
				element: <Dashboard />,
			},
			{
				path: "/table",
				element: <TableComponent />,
			},
		],
	},
]);
