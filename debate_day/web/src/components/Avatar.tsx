import React from 'react';

interface AvatarProps {
  sender: 'Pro' | 'Con' | 'Moderator';
}

const Avatar: React.FC<AvatarProps> = ({ sender }) => {
  const getAvatarText = () => {
    if (sender === 'Pro') return 'P';
    if (sender === 'Con') return 'C';
    if (sender === 'Moderator') return 'M';
    return '?';
  };

  const getAvatarColor = () => {
    if (sender === 'Pro') return 'bg-blue-500';
    if (sender === 'Con') return 'bg-red-500';
    if (sender === 'Moderator') return 'bg-green-500';
    return 'bg-gray-500';
  };

  return (
    <div className={`w-10 h-10 rounded-full flex items-center justify-center text-white font-bold ${getAvatarColor()}`}>
      {getAvatarText()}
    </div>
  );
};

export default Avatar; 