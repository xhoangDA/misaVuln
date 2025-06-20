import { useState, useEffect } from 'react';
import axios from 'axios';

export default function HistoryTable() {
  const [history, setHistory] = useState([]);

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const { data } = await axios.get('/api/history/');
        setHistory(data);
      } catch (error) {
        console.error('Error fetching history:', error);
      }
    };
    fetchHistory();
  }, []);

  return (
    <div className="overflow-x-auto">
      <table className="min-w-full bg-white">
        <thead>
          <tr>
            <th className="py-2 px-4 border">Filename</th>
            <th className="py-2 px-4 border">Status</th>
            <th className="py-2 px-4 border">Processed At</th>
            <th className="py-2 px-4 border">Actions</th>
          </tr>
        </thead>
        <tbody>
          {history.map((item) => (
            <tr key={item.id}>
              <td className="py-2 px-4 border">{item.original_filename}</td>
              <td className="py-2 px-4 border">
                <span className={`px-2 py-1 rounded-full text-xs ${
                  item.status === 'COMPLETED' ? 'bg-green-100 text-green-800' :
                  item.status === 'FAILED' ? 'bg-red-100 text-red-800' :
                  'bg-yellow-100 text-yellow-800'
                }`}>
                  {item.status}
                </span>
              </td>
              <td className="py-2 px-4 border">
                {new Date(item.completed_at).toLocaleString()}
              </td>
              <td className="py-2 px-4 border">
                {item.status === 'COMPLETED' && (
                  <a 
                    href={`/api/download/${item.id}`}
                    className="text-blue-600 hover:underline"
                  >
                    Download
                  </a>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}