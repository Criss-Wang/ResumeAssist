'use client';
import { useState } from 'react';
import { TextField, Typography, Box, Button, Divider } from '@mui/material';
import { green } from "@mui/material/colors"

export default function PersonalInfo({ onResumeChange, resume }) {
    const [personalInfo, setBasicInfo] = useState({});
    const handleChange = (field) => (event) => {
        const { value } = event.target;
        setBasicInfo({
            ...personalInfo,
            [field]: value,
        });
    };

    const handleSaveAll = async () => {
        onResumeChange({
            ...resume,
            personal_info: personalInfo
        });
        
        try {
            // Send a POST request to your backend
            const response = await fetch(`/api/personal-info/save/${resume.id}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(personalInfo),
            });
            
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
        } catch (error) {
            console.error('Failed to refresh PDF:', error);
        }
    }

    return (
        <Box className="mb-6">
          <Divider sx={{ borderBottomWidth: '2px'}}/>
          <Box display="flex" className="gap-2 mt-1" alignItems="center" mb={1}>
                <Typography variant="h6" className="pb-2 pt-4" flexGrow={1}>Personal Information</Typography>
                <Button
                    variant="contained"
                    size="small"
                    sx={{ 
                        backgroundColor: green[300],
                        '&:hover': {
                        backgroundColor: green[500], // Change color on hover
                        },
                    }}
                    onClick={handleSaveAll}
                >
                    Save All
                </Button>
            </Box>
            <Box className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-3">
                <div className="flex flex-col space-y-4">
                    <TextField label="Name" variant="outlined" size="small" fullWidth onChange={handleChange('name')}/>
                    <TextField label="Email" variant="outlined" size="small" fullWidth onChange={handleChange('email')}/>
                    <TextField label="Telephone" variant="outlined" size="small" fullWidth onChange={handleChange('phone')}/>
                </div>
                <div className="flex flex-col space-y-4">
                    <TextField label="LinkedIn" variant="outlined" size="small" fullWidth onChange={handleChange('linkedin')}/>
                    <TextField label="GitHub" variant="outlined" size="small" fullWidth onChange={handleChange('github')}/>
                    <TextField label="Personal Website" variant="outlined" size="small" fullWidth onChange={handleChange('website')}/>
                </div>
            </Box>
        </Box>
    )
}