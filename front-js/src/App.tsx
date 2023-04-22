import React from 'react';
import {createTheme, ThemeProvider} from "@mui/material";
import HomePage from "./pages/HomePage";
import {ROUTES} from "./routes/routes";
import {Navigate, Route, Routes} from "react-router";
import {ResultsPage} from "./pages/ResultsPage";

const theme = createTheme();

function App() {
    return (
        <>
            <ThemeProvider theme={theme}>
                <Routes>
                    <Route path={ROUTES.HOME} element={<HomePage />} />
                    <Route path={ROUTES.RESULTS} element={<ResultsPage />} />
                    <Route path={ROUTES.ROOT} element={<Navigate to={ROUTES.HOME} />} />
                </Routes>
            </ThemeProvider>
        </>
    );
}

export default App;
