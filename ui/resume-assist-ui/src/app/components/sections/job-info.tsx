'use client';
import { TextField, Typography, Box, Paper } from '@mui/material';

export default function JobInfo() {
    return (
        <Paper elevation={3} className="w-full p-4 mt-5 mb-6">
            <Typography variant="h5" className="mb-12 pb-4">
                Job Details
            </Typography>
            <Box component="form" className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="flex flex-col space-y-4">
                <TextField label="Job Title" variant="outlined" fullWidth />
                <TextField label="Company Name" variant="outlined" fullWidth />
            </div>
            <TextField
                label="Job Description"
                variant="outlined"
                multiline
                rows={4}
                fullWidth
            />
            </Box>
        </Paper>
    )
}