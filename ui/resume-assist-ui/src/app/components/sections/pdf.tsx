'use client';
import { useState } from 'react';
import { Box, Button, Typography } from '@mui/material';
import RefreshIcon from '@mui/icons-material/Refresh';

export default function PDFSection({ resume, job }) {
    const [pdfPath, setPdfPath] = useState("");
    const [pdfKey, setPdfKey] = useState(1);
    const saveResume = async () => {
        try {
            console.log({ ...resume, job_details: job});
            
            const response = await fetch(`/api/resume/save/${resume.id}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ ...resume, job_details: job}),
            });
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            setPdfKey(-1 * pdfKey);
            setPdfPath(`/pdf/${resume.personal_info.name.replace(" ", "")}_Resume.pdf`);
        }   catch (error) {
              console.error('Failed to refresh PDF:', error);
        }
    };

    return (
        <Box className="mb-6">
            <Box display="flex" justifyContent="space-between" alignItems="center">
                <Typography variant="h5">Resume/CV Viewer</Typography>
                <Box>
                    <Button
                        variant="contained"
                        color="secondary"
                        onClick={saveResume}
                        sx={{ ml: 1 }}
                    >
                        Save Resume & Refresh <RefreshIcon />
                    </Button>
                    {/* <Button
                        variant="contained"
                        color="primary"
                        onClick={refreshPDF}
                        sx={{ ml: 1 }}
                    >
                        Refresh PDF &nbsp; <RefreshIcon />
                    </Button> */}
                </Box>
            </Box>
            <Box mt={4}>
                <object className="min-w-full" height="1200" data={pdfPath} key={pdfKey} type="application/pdf">
                    
                </object>
            </Box>
        </Box>
    );
}
