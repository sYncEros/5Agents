import { motion } from "framer-motion";
import type { Role } from "../../../shared/organizational-levels";

interface RoleCardProps {
  role: Role;
  index: number;
  isCompact?: boolean;
}

const colorMap: Record<string, { bg: string; border: string; text: string }> = {
  blue: {
    bg: "bg-blue-500/10",
    border: "border-blue-500",
    text: "text-blue-400",
  },
  purple: {
    bg: "bg-purple-500/10",
    border: "border-purple-500",
    text: "text-purple-400",
  },
  pink: {
    bg: "bg-pink-500/10",
    border: "border-pink-500",
    text: "text-pink-400",
  },
  green: {
    bg: "bg-green-500/10",
    border: "border-green-500",
    text: "text-green-400",
  },
  emerald: {
    bg: "bg-emerald-500/10",
    border: "border-emerald-500",
    text: "text-emerald-400",
  },
  cyan: {
    bg: "bg-cyan-500/10",
    border: "border-cyan-500",
    text: "text-cyan-400",
  },
  amber: {
    bg: "bg-amber-500/10",
    border: "border-amber-500",
    text: "text-amber-400",
  },
  indigo: {
    bg: "bg-indigo-500/10",
    border: "border-indigo-500",
    text: "text-indigo-400",
  },
  yellow: {
    bg: "bg-yellow-500/10",
    border: "border-yellow-500",
    text: "text-yellow-400",
  },
  slate: {
    bg: "bg-slate-500/10",
    border: "border-slate-500",
    text: "text-slate-400",
  },
  teal: {
    bg: "bg-teal-500/10",
    border: "border-teal-500",
    text: "text-teal-400",
  },
  violet: {
    bg: "bg-violet-500/10",
    border: "border-violet-500",
    text: "text-violet-400",
  },
  rose: {
    bg: "bg-rose-500/10",
    border: "border-rose-500",
    text: "text-rose-400",
  },
  orange: {
    bg: "bg-orange-500/10",
    border: "border-orange-500",
    text: "text-orange-400",
  },
  fuchsia: {
    bg: "bg-fuchsia-500/10",
    border: "border-fuchsia-500",
    text: "text-fuchsia-400",
  },
  lime: {
    bg: "bg-lime-500/10",
    border: "border-lime-500",
    text: "text-lime-400",
  },
  gray: {
    bg: "bg-gray-500/10",
    border: "border-gray-500",
    text: "text-gray-400",
  },
  red: { bg: "bg-red-500/10", border: "border-red-500", text: "text-red-400" },
};

export default function RoleCard({
  role,
  index,
  isCompact = false,
}: RoleCardProps) {
  const colors = colorMap[role.color] || colorMap.blue;

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.9, y: 20 }}
      animate={{ opacity: 1, scale: 1, y: 0 }}
      transition={{ delay: index * 0.05, duration: 0.3 }}
      className={`${colors.bg} ${colors.border} border-2 rounded-xl p-4 hover:scale-105 transition-transform cursor-pointer`}
    >
      <div className="flex items-start gap-3">
        <div className="text-4xl">{role.icon}</div>
        <div className="flex-1 min-w-0">
          <h3
            className={`font-semibold ${colors.text} ${isCompact ? "text-sm" : "text-base"}`}
          >
            {role.name}
          </h3>
          <p
            className={`text-gray-400 ${isCompact ? "text-xs mt-0.5" : "text-sm mt-1"} line-clamp-2`}
          >
            {role.description}
          </p>

          {!isCompact && (
            <>
              <div className="mt-3 space-y-1">
                <p className="text-xs text-gray-500 font-medium">
                  Responsabilidades:
                </p>
                <ul className="text-xs text-gray-400 space-y-0.5">
                  {role.responsibilities.slice(0, 2).map((resp, i) => (
                    <li key={i} className="flex items-start gap-1">
                      <span className={colors.text}>•</span>
                      <span>{resp}</span>
                    </li>
                  ))}
                </ul>
              </div>

              <div className="mt-3 flex flex-wrap gap-1">
                {role.skills.slice(0, 3).map((skill, i) => (
                  <span
                    key={i}
                    className={`text-xs px-2 py-0.5 rounded-full ${colors.bg} ${colors.text} border ${colors.border}`}
                  >
                    {skill}
                  </span>
                ))}
              </div>
            </>
          )}
        </div>
      </div>
    </motion.div>
  );
}
