'use client';
import { TextField, Typography, Box } from '@mui/material';

export default function PersonalInfo() {
    return (
        <Box className="mb-6">
            <Typography variant="h6" className="mb-2">Background</Typography>
            <Box className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="flex flex-col space-y-4">
                <TextField label="Name" variant="outlined" fullWidth />
                <TextField label="Email" variant="outlined" fullWidth />
                <TextField label="Telephone" variant="outlined" fullWidth />
            </div>
            <div className="flex flex-col space-y-4">
                <TextField label="LinkedIn" variant="outlined" fullWidth />
                <TextField label="GitHub" variant="outlined" fullWidth />
                <TextField label="Personal Website" variant="outlined" fullWidth />
            </div>
            </Box>
        </Box>
    )
}