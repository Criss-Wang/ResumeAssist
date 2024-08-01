'use client';
import { TextField, Typography, Box } from '@mui/material';

export default function PersonalInfo({ onResumeChange, resume }) {
    const handleChange = (field) => (event) => {
        const { value } = event.target;
        onResumeChange({
            ...resume,
            [field]: value,
        });
    };

    return (
        <Box className="mb-6">
            <Typography variant="h6" className="mb-2">Background</Typography>
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