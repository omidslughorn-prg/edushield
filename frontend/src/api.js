import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:8000';

export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const getTodayAttendance = () => api.get('/attendance/today');
export const recordAttendance = (data) => api.post('/attendance/record', data);
export const requestOTP = (data) => api.post('/otp/request', data);
export const verifyOTP = (data) => api.post('/otp/verify', data);
export const createExitPermit = (data) => api.post('/exit-permits/create', data);