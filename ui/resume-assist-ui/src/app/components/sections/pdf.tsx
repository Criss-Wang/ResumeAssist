import React from 'react';
import { Box, Button, Typography } from '@mui/material';
import RefreshIcon from '@mui/icons-material/Refresh';

export default function PDFSection({ resume }) {
    const refreshPDF = async () => {
        try {
            // Send a POST request to your backend
            const response = await fetch('/pdf/render', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ "resume": resume }), // Replace with your payload if needed
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
        } catch (error) {
            console.error('Failed to refresh PDF:', error);
        }
    };

    const pdfPath = '/pdf/cv.pdf';
    return (
        <Box className="mb-6">
            <Box display="flex" justifyContent="space-between" alignItems="center">
                <Typography variant="h5">Resume/CV Viewer</Typography>
                <Box>
                    <Button
                        variant="contained"
                        color="secondary"
                        onClick={refreshPDF}
                        sx={{ ml: 1 }}
                    >
                        Save Resume
                    </Button>
                    <Button
                        variant="contained"
                        color="primary"
                        onClick={refreshPDF}
                        sx={{ ml: 1 }}
                    >
                        <RefreshIcon />
                    </Button>
                </Box>
            </Box>
            <Box mt={4}>
                <object className="min-w-full" height="1200" data={pdfPath} type="application/pdf">
                    
                </object>
            </Box>
        </Box>
    );
}
