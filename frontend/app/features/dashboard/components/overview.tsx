import React from "react";
import { Link } from "react-router";
import { 
  FileText, 
  Mic, 
  Sparkles, 
  Plus,
  Clock,
  TrendingUp,
  BookOpen
} from "lucide-react";
import { Button } from "~/components/ui/button";

export function DashboardOverview() {
  // Temporary static data for testing
  // const recentNotes = useRecentNotes(3);
  // const recentRecordings = useRecentRecordings(2);
  // const recentSummaries = useRecentSummaries(3);

  // Mock data for testing
  const recentNotes = [
    { 
      id: '1', 
      title: 'Meeting Notes - Q4 Planning', 
      updatedAt: new Date(), 
      createdAt: new Date(),
      content: 'Team meeting...', 
      excerpt: 'Important Q4 planning discussion with key stakeholders...',
      type: 'text'
    },
    { 
      id: '2', 
      title: 'Project Ideas', 
      updatedAt: new Date(), 
      createdAt: new Date(),
      content: 'New feature ideas...', 
      excerpt: 'Brainstorming session for new product features...',
      type: 'text'
    },
    { 
      id: '3', 
      title: 'Research Notes', 
      updatedAt: new Date(), 
      createdAt: new Date(),
      content: 'Market research...', 
      excerpt: 'Comprehensive market analysis and user research findings...',
      type: 'text'
    }
  ];
  
  const recentRecordings = [
    { 
      id: '1', 
      title: 'Voice Memo - Ideas', 
      createdAt: new Date(), 
      duration: 120,
      transcription: 'Quick voice note about new product ideas and improvements'
    },
    { 
      id: '2', 
      title: 'Meeting Recording', 
      createdAt: new Date(), 
      duration: 300,
      transcription: 'Important team meeting discussion about project roadmap'
    }
  ];
  
  const recentSummaries = [
    { id: '1', title: 'Weekly Summary', createdAt: new Date(), content: 'This week summary...' },
    { id: '2', title: 'Project Summary', createdAt: new Date(), content: 'Project overview...' },
    { id: '3', title: 'Research Summary', createdAt: new Date(), content: 'Key findings...' }
  ];

  // Static stats for testing
  const stats = [
    {
      title: "Total Notes",
      value: "12",
      change: "+12%",
      icon: FileText,
      color: "text-blue-600",
      bgColor: "bg-blue-50",
    },
    {
      title: "Voice Recordings",
      value: "8",
      change: "+23%",
      icon: Mic,
      color: "text-green-600",
      bgColor: "bg-green-50",
    },
    {
      title: "AI Summaries",
      value: "5",
      change: "+8%",
      icon: Sparkles,
      color: "text-purple-600",
      bgColor: "bg-purple-50",
    },
    {
      title: "Reading Time",
      value: "2.5h",
      change: "+15%",
      icon: Clock,
      color: "text-orange-600",
      bgColor: "bg-orange-50",
    },
  ];

  // Format time ago
  const formatTimeAgo = (date: Date) => {
    const now = new Date();
    const diffInMinutes = Math.floor((now.getTime() - date.getTime()) / (1000 * 60));
    
    if (diffInMinutes < 60) {
      return `${diffInMinutes} minutes ago`;
    } else if (diffInMinutes < 1440) {
      const hours = Math.floor(diffInMinutes / 60);
      return `${hours} hour${hours > 1 ? 's' : ''} ago`;
    } else {
      const days = Math.floor(diffInMinutes / 1440);
      return `${days} day${days > 1 ? 's' : ''} ago`;
    }
  };

  const quickActions = [
    {
      title: "New Note",
      description: "Create a new text note",
      href: "/notes/new",
      icon: FileText,
      color: "bg-blue-500"
    },
    {
      title: "Voice Recording",
      description: "Start recording audio",
      href: "/voice/record",
      icon: Mic,
      color: "bg-green-500"
    },
    {
      title: "AI Summary",
      description: "Generate AI-powered summary",
      href: "/dashboard/ai",
      icon: Sparkles,
      color: "bg-purple-500"
    }
  ];

  return (
    <div className="p-6 space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-gray-900 dark:text-white font-jakarta">
          Welcome back! 👋
        </h1>
        <p className="text-gray-600 dark:text-gray-400 mt-1">
          Here's what's happening with your notes today.
        </p>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {stats.map((stat, index) => (
          <div
            key={index}
            className="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-sm border border-gray-200 dark:border-gray-700 hover:shadow-md transition-shadow"
          >
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600 dark:text-gray-400">
                  {stat.title}
                </p>
                <p className="text-2xl font-bold text-gray-900 dark:text-white mt-1">
                  {stat.value}
                </p>
                <div className="flex items-center mt-2">
                  <TrendingUp className="w-4 h-4 text-green-500 mr-1" />
                  <span className="text-sm text-green-600 font-medium">
                    {stat.change}
                  </span>
                </div>
              </div>
              <div className={`${stat.bgColor} ${stat.color} p-3 rounded-lg`}>
                <stat.icon className="w-6 h-6" />
              </div>
            </div>
          </div>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Recent Notes */}
        <div className="lg:col-span-2">
          <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700">
            <div className="p-6 border-b border-gray-200 dark:border-gray-700">
              <div className="flex items-center justify-between">
                <h2 className="text-lg font-semibold text-gray-900 dark:text-white">
                  Recent Notes
                </h2>
                <Link to="/notes">
                  <Button variant="outline" size="sm">
                    View All
                  </Button>
                </Link>
              </div>
            </div>
            <div className="p-6">
              <div className="space-y-4">
                {recentNotes.map((note) => (
                  <Link 
                    key={note.id}
                    to={`/notes/${note.id}`}
                    className="block p-4 rounded-lg border border-gray-200 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors"
                  >
                    <div className="flex items-start gap-3">
                      <div className="w-10 h-10 bg-[#034391]/10 rounded-lg flex items-center justify-center flex-shrink-0">
                        {note.type === "voice" ? (
                          <Mic className="w-5 h-5 text-[#034391]" />
                        ) : (
                          <FileText className="w-5 h-5 text-[#034391]" />
                        )}
                      </div>
                      <div className="flex-1 min-w-0">
                        <h3 className="font-medium text-gray-900 dark:text-white truncate">
                          {note.title}
                        </h3>
                        <p className="text-sm text-gray-600 dark:text-gray-400 mt-1 line-clamp-2">
                          {note.excerpt}
                        </p>
                        <p className="text-xs text-gray-500 mt-2">
                          {formatTimeAgo(note.createdAt)}
                        </p>
                      </div>
                    </div>
                  </Link>
                ))}
                
                {/* Show recent recordings as well */}
                {recentRecordings.map((recording) => (
                  <Link 
                    key={recording.id}
                    to={`/voice/${recording.id}`}
                    className="block p-4 rounded-lg border border-gray-200 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors"
                  >
                    <div className="flex items-start gap-3">
                      <div className="w-10 h-10 bg-[#034391]/10 rounded-lg flex items-center justify-center flex-shrink-0">
                        <Mic className="w-5 h-5 text-[#034391]" />
                      </div>
                      <div className="flex-1 min-w-0">
                        <h3 className="font-medium text-gray-900 dark:text-white truncate">
                          {recording.title}
                        </h3>
                        <p className="text-sm text-gray-600 dark:text-gray-400 mt-1 line-clamp-2">
                          {recording.transcription || `Duration: ${Math.floor(recording.duration / 60)}:${(recording.duration % 60).toString().padStart(2, '0')}`}
                        </p>
                        <p className="text-xs text-gray-500 mt-2">
                          {formatTimeAgo(recording.createdAt)}
                        </p>
                      </div>
                    </div>
                  </Link>
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* Quick Actions */}
        <div>
          <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700">
            <div className="p-6 border-b border-gray-200 dark:border-gray-700">
              <h2 className="text-lg font-semibold text-gray-900 dark:text-white">
                Quick Actions
              </h2>
            </div>
            <div className="p-6">
              <div className="space-y-3">
                {quickActions.map((action, index) => (
                  <Link
                    key={index}
                    to={action.href}
                    className="flex items-center gap-3 p-3 rounded-lg border border-gray-200 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors group"
                  >
                    <div className={`${action.color} p-2 rounded-lg text-white group-hover:scale-105 transition-transform`}>
                      <action.icon className="w-4 h-4" />
                    </div>
                    <div>
                      <h3 className="font-medium text-gray-900 dark:text-white text-sm">
                        {action.title}
                      </h3>
                      <p className="text-xs text-gray-600 dark:text-gray-400">
                        {action.description}
                      </p>
                    </div>
                  </Link>
                ))}
              </div>
            </div>
          </div>

          {/* Activity Summary */}
          <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 mt-6">
            <div className="p-6 border-b border-gray-200 dark:border-gray-700">
              <h2 className="text-lg font-semibold text-gray-900 dark:text-white">
                Today's Activity
              </h2>
            </div>
            <div className="p-6">
              <div className="space-y-4">
                <div className="flex items-center gap-3">
                  <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                  <span className="text-sm text-gray-600 dark:text-gray-400">
                    3 notes created
                  </span>
                </div>
                <div className="flex items-center gap-3">
                  <div className="w-2 h-2 bg-blue-500 rounded-full"></div>
                  <span className="text-sm text-gray-600 dark:text-gray-400">
                    2 voice recordings
                  </span>
                </div>
                <div className="flex items-center gap-3">
                  <div className="w-2 h-2 bg-purple-500 rounded-full"></div>
                  <span className="text-sm text-gray-600 dark:text-gray-400">
                    1 AI summary generated
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}