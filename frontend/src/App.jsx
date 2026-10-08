import React, { useState, useEffect } from 'react';
import {
  UserCheck,
  Clock,
  UserX,
  AlertCircle,
  CheckCircle2,
} from 'lucide-react';

import { recordAttendance, getTodayAttendance } from './api';

export default function App() {
  const [studentId, setStudentId] = useState('STU-980124');
  const [status, setStatus] = useState('late');
  const [entryTime, setEntryTime] = useState('07:45');
  const [delayMinutes, setDelayMinutes] = useState(15);
  const [description, setDescription] = useState('');

  const [records, setRecords] = useState([]);
  const [message, setMessage] = useState(null);
  const [loading, setLoading] = useState(false);

  const fetchRecords = async () => {
    try {
      const res = await getTodayAttendance();
      setRecords(res.data);
    } catch (err) {
      console.error('Error fetching today records:', err);
    }
  };

  useEffect(() => {
    fetchRecords();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();

    setLoading(true);
    setMessage(null);

    const payload = {
      student_id: studentId,
      record_date: new Date().toISOString().split('T')[0],
      entry_time: status === 'late' ? entryTime : null,
      delay_minutes:
        status === 'late' ? parseInt(delayMinutes, 10) || 0 : 0,
      status: status,
      description: description || null,
    };

    try {
      await recordAttendance(payload);

      setMessage({
        type: 'success',
        text: 'ثبت تاخیر/غیبت با موفقیت انجام شد و پیامک برای ولی ارسال گردید.',
      });

      await fetchRecords();

      // پاک کردن توضیحات بعد از ثبت
      setDescription('');
    } catch (err) {
      setMessage({
        type: 'error',
        text:
          err.response?.data?.detail ||
          'خطا در ثبت اطلاعات',
      });
    } finally {
      setLoading(false);
    }
  };

  // تابع دریافت و دانلود فایل اکسل
  const handleDownloadExcel = async () => {
    try {
      const today = new Date().toISOString().split('T')[0];
      const response = await fetch(
        `http://localhost:8000/reports/excel/attendance?start_date=${today}&end_date=${today}`
      );

      if (!response.ok) {
        throw new Error('خطا در دریافت فایل اکسل');
      }

      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `Attendance_Report_${today}.xlsx`;
      document.body.appendChild(a);
      a.click();
      a.remove();
      window.URL.revokeObjectURL(url);
    } catch (error) {
      console.error('Download error:', error);
      alert('خطا در دریافت خروجی اکسل');
    }
  };

  return (
    <div
      dir="rtl"
      className="min-h-screen bg-slate-100 text-slate-800"
    >
      {/* Header */}
      <header className="bg-slate-900 text-white shadow-lg">
        <div className="max-w-5xl mx-auto px-4 py-6">
          <h1 className="text-2xl md:text-3xl font-bold">
            سامانه ناظم‌همراه
          </h1>

          <p className="mt-2 text-slate-300">
            ثبت تاخیر و غیبت حیاط / صف مدرسه
          </p>
        </div>
      </header>

      <main className="max-w-5xl mx-auto px-4 py-6 space-y-6">
        {/* Feedback Message */}
        {message && (
          <div
            className={`flex items-center gap-3 p-4 rounded-xl border ${
              message.type === 'success'
                ? 'bg-green-50 border-green-200 text-green-800'
                : 'bg-red-50 border-red-200 text-red-800'
            }`}
          >
            {message.type === 'success' ? (
              <CheckCircle2 className="w-5 h-5 shrink-0" />
            ) : (
              <AlertCircle className="w-5 h-5 shrink-0" />
            )}

            <span>{message.text}</span>
          </div>
        )}

        {/* Quick Attendance Form */}
        <section className="bg-white rounded-2xl shadow-sm border border-slate-200 p-5 md:p-6">
          <h2 className="text-xl font-bold mb-6">
            ثبت تاخیر / غیبت جدید
          </h2>

          <form onSubmit={handleSubmit} className="space-y-6">
            {/* Student ID */}
            <div>
              <label
                htmlFor="studentId"
                className="block mb-2 font-medium"
              >
                شناسه دانش‌آموز
              </label>

              <input
                id="studentId"
                type="text"
                value={studentId}
                onChange={(e) => setStudentId(e.target.value)}
                className="w-full p-3 border border-slate-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none"
                placeholder="مثال: STU-980124"
                required
              />
            </div>

            {/* Status Selector */}
            <div>
              <label className="block mb-3 font-medium">
                وضعیت حضور و غیاب
              </label>

              <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
                {/* Late */}
                <button
                  type="button"
                  onClick={() => setStatus('late')}
                  className={`p-4 rounded-xl border flex flex-col items-center justify-center gap-2 font-medium text-sm transition-all ${
                    status === 'late'
                      ? 'bg-amber-500 text-white border-amber-500 shadow-md'
                      : 'border-slate-200 text-slate-600 hover:bg-slate-50'
                  }`}
                >
                  <Clock className="w-6 h-6" />
                  <span>تاخیر ورود</span>
                </button>

                {/* Unexcused */}
                <button
                  type="button"
                  onClick={() => setStatus('unexcused')}
                  className={`p-4 rounded-xl border flex flex-col items-center justify-center gap-2 font-medium text-sm transition-all ${
                    status === 'unexcused'
                      ? 'bg-red-500 text-white border-red-500 shadow-md'
                      : 'border-slate-200 text-slate-600 hover:bg-slate-50'
                  }`}
                >
                  <UserX className="w-6 h-6" />
                  <span>غیبت غیرموجه</span>
                </button>

                {/* Excused */}
                <button
                  type="button"
                  onClick={() => setStatus('excused')}
                  className={`p-4 rounded-xl border flex flex-col items-center justify-center gap-2 font-medium text-sm transition-all ${
                    status === 'excused'
                      ? 'bg-blue-500 text-white border-blue-500 shadow-md'
                      : 'border-slate-200 text-slate-600 hover:bg-slate-50'
                  }`}
                >
                  <UserCheck className="w-6 h-6" />
                  <span>غیبت موجه</span>
                </button>
              </div>
            </div>

            {/* Late-specific inputs */}
            {status === 'late' && (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {/* Entry Time */}
                <div>
                  <label
                    htmlFor="entryTime"
                    className="block mb-2 font-medium"
                  >
                    زمان ورود
                  </label>

                  <input
                    id="entryTime"
                    type="time"
                    value={entryTime}
                    onChange={(e) => setEntryTime(e.target.value)}
                    className="w-full p-3 border border-slate-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none"
                    required
                  />
                </div>

                {/* Delay */}
                <div>
                  <label
                    htmlFor="delayMinutes"
                    className="block mb-2 font-medium"
                  >
                    میزان تاخیر (دقیقه)
                  </label>

                  <input
                    id="delayMinutes"
                    type="number"
                    min="0"
                    value={delayMinutes}
                    onChange={(e) => setDelayMinutes(e.target.value)}
                    className="w-full p-3 border border-slate-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none"
                    required
                  />
                </div>
              </div>
            )}

            {/* Description */}
            <div>
              <label
                htmlFor="description"
                className="block mb-2 font-medium"
              >
                توضیحات / علت (اختیاری)
              </label>

              <textarea
                id="description"
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                rows="3"
                className="w-full p-3 border border-slate-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none resize-none"
                placeholder="توضیح مختصر در صورت نیاز..."
              />
            </div>

            {/* Submit */}
            <button
              type="submit"
              disabled={loading}
              className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-slate-400 disabled:cursor-not-allowed text-white font-bold py-3 px-5 rounded-xl transition-colors"
            >
              {loading
                ? 'در حال ثبت...'
                : 'ثبت و ارسال پیامک خودکار به ولی'}
            </button>
          </form>
        </section>

        {/* Today Records List */}
        <section className="bg-white rounded-2xl shadow-sm border border-slate-200 p-5 md:p-6">
          <div className="flex justify-between items-center mb-4">
            <h3 className="text-lg font-bold">
              لیست ثبت‌شده‌های امروز
            </h3>
            <button
              type="button"
              onClick={handleDownloadExcel}
              className="bg-emerald-600 hover:bg-emerald-700 text-white px-3 py-1.5 rounded-xl text-sm font-medium flex items-center gap-2 transition-colors"
            >
              📊 دریافت خروجی اکسل
            </button>
          </div>

          {records.length === 0 ? (
            <div className="text-center py-8 text-slate-500">
              هیچ رکوردی برای امروز ثبت نشده است.
            </div>
          ) : (
            <div className="space-y-3">
              {records.map((rec, index) => (
                <div
                  key={rec.id ?? `${rec.student_id}-${index}`}
                  className="flex flex-col md:flex-row md:items-center md:justify-between gap-3 p-4 rounded-xl bg-slate-50 border border-slate-200"
                >
                  <div>
                    <div className="font-bold text-slate-800">
                      {rec.student_id}
                    </div>

                    <div className="text-sm text-slate-500 mt-1">
                      زمان ورود: {rec.entry_time || '-'} | تاخیر:{' '}
                      {rec.delay_minutes || 0} دقیقه
                    </div>
                  </div>

                  <div
                    className={`inline-flex self-start md:self-auto px-3 py-1 rounded-full text-sm font-medium ${
                      rec.status === 'late'
                        ? 'bg-amber-100 text-amber-700'
                        : rec.status === 'unexcused'
                        ? 'bg-red-100 text-red-700'
                        : 'bg-blue-100 text-blue-700'
                    }`}
                  >
                    {rec.status === 'late'
                      ? 'تاخیر ورود'
                      : rec.status === 'unexcused'
                      ? 'غیبت غیرموجه'
                      : 'غیبت موجه'}
                  </div>
                </div>
              ))}
            </div>
          )}
        </section>
      </main>
    </div>
  );
}