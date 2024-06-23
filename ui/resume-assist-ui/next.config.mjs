/** @type {import('next').NextConfig} */
const nextConfig = {
    output: 'export', // <=== enables static exports
    reactStrictMode: false,
    images: {
        unoptimized: true, // <==  disable server-based image optimization
  },
};

export default nextConfig;
