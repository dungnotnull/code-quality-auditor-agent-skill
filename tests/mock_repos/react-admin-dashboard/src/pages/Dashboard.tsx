// src/pages/Dashboard.tsx - FLAWED: Performance issues (unnecessary re-renders, large bundle)

import React, { useState, useEffect } from 'react';
import { useUsers } from '../hooks/useUsers';

// FLAW: Large inline component - should be split
export const Dashboard: React.FC = () => {
  const { users, isLoading } = useUsers();
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedFilter, setSelectedFilter] = useState('all');
  const [sortField, setSortField] = useState('name');
  const [sortDirection, setSortDirection] = useState<'asc' | 'desc'>('asc');
  const [currentPage, setCurrentPage] = useState(1);
  const [itemsPerPage, setItemsPerPage] = useState(20);

  // FLAW: Expensive computation on every render without useMemo
  const filteredUsers = users
    .filter((user: any) => {  // FLAW: Using 'any' type - no type safety
      if (searchTerm) {
        return user.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
               user.email.toLowerCase().includes(searchTerm.toLowerCase());
      }
      return true;
    })
    .filter((user: any) => {
      if (selectedFilter !== 'all') {
        return user.role === selectedFilter;
      }
      return true;
    })
    .sort((a: any, b: any) => {  // FLAW: Sort on every render
      const aVal = a[sortField];
      const bVal = b[sortField];
      const direction = sortDirection === 'asc' ? 1 : -1;
      return String(aVal).localeCompare(String(bVal)) * direction;
    });

  // FLAW: Pagination computed on every render
  const startIndex = (currentPage - 1) * itemsPerPage;
  const paginatedUsers = filteredUsers.slice(startIndex, startIndex + itemsPerPage);

  if (isLoading) {
    return <div>Loading...</div>;  // FLAW: No skeleton/progressive loading
  }

  return (
    <div className="dashboard" style={{ padding: '20px', maxWidth: '1200px', margin: '0 auto' }}>
      {/* FLAW: Inline styles instead of CSS modules or styled-components */}
      <h1 style={{ fontSize: '24px', marginBottom: '16px' }}>Admin Dashboard</h1>

      <div style={{ marginBottom: '16px', display: 'flex', gap: '12px' }}>
        <input
          type="text"
          placeholder="Search users..."
          value={searchTerm}
          onChange={(e) => {
            setSearchTerm(e.target.value);
            setCurrentPage(1);  // FLAW: Reset page on every keystroke
          }}
          style={{ padding: '8px', border: '1px solid #ccc', borderRadius: '4px' }}
        />
        <select
          value={selectedFilter}
          onChange={(e) => setSelectedFilter(e.target.value)}
          style={{ padding: '8px', border: '1px solid #ccc', borderRadius: '4px' }}
        >
          <option value="all">All Roles</option>
          <option value="admin">Admin</option>
          <option value="user">User</option>
        </select>
      </div>

      <table style={{ width: '100%', borderCollapse: 'collapse' }}>
        <thead>
          <tr>
            <th onClick={() => setSortField('name')} style={{ cursor: 'pointer' }}>Name</th>
            <th onClick={() => setSortField('email')} style={{ cursor: 'pointer' }}>Email</th>
            <th>Role</th>
          </tr>
        </thead>
        <tbody>
          {/* FLAW: No React.memo on row component - re-renders all rows on any state change */}
          {paginatedUsers.map((user: any) => (
            <tr key={user.id} style={{ borderBottom: '1px solid #eee' }}>
              <td style={{ padding: '8px' }}>{user.name}</td>
              <td style={{ padding: '8px' }}>{user.email}</td>
              <td style={{ padding: '8px' }}>{user.role}</td>
            </tr>
          ))}
        </tbody>
      </table>

      {/* FLAW: Pagination controls without accessibility (no aria labels) */}
      <div style={{ marginTop: '16px', display: 'flex', gap: '8px' }}>
        {Array.from({ length: Math.ceil(filteredUsers.length / itemsPerPage) }, (_, i) => (
          <button
            key={i}
            onClick={() => setCurrentPage(i + 1)}
            style={{
              padding: '4px 8px',
              border: '1px solid #ccc',
              background: currentPage === i + 1 ? '#007bff' : 'white',
              color: currentPage === i + 1 ? 'white' : 'black',
            }}
          >
            {i + 1}
          </button>
        ))}
      </div>
    </div>
  );
};
