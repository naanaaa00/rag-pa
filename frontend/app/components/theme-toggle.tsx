import { Moon, Sun } from "lucide-react";
import { Button } from "~/components/ui/button";
import { useTheme } from "~/providers/theme-provider";

interface ThemeToggleProps {
  className?: string;
  variant?: "default" | "outline" | "ghost";
}

export function ThemeToggle({ className, variant = "outline" }: ThemeToggleProps) {
  const { theme, setTheme } = useTheme();

  const toggleTheme = () => {
    if (theme === "light") {
      setTheme("dark");
    } else if (theme === "dark") {
      setTheme("system");
    } else {
      setTheme("light");
    }
  };

  return (
    <Button 
      variant={variant} 
      size="icon" 
      onClick={toggleTheme}
      className={className || (variant === "outline" ? "bg-white/10 border-white/20 hover:bg-white/20 text-white" : "")}
    >
      <Sun className="h-[1.2rem] w-[1.2rem] rotate-0 scale-100 transition-all dark:-rotate-90 dark:scale-0" />
      <Moon className="absolute h-[1.2rem] w-[1.2rem] rotate-90 scale-0 transition-all dark:rotate-0 dark:scale-100" />
      <span className="sr-only">Toggle theme</span>
    </Button>
  );
}