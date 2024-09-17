/** @type {import('next').NextConfig} */
const nextConfig = {
    reactStrictMode: false,
    images: {
        unoptimized: true, // <==  disable server-based image optimization
    },
    async redirects() {
      return [
        {
          source: '/api/:path*',
          destination: 'http://localhost:10010/api/:path*',
          permanent: false
        },
      ]
    },
};

export default nextConfig;
