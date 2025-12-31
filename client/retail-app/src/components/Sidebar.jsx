import { Link } from "react-router-dom";
import { BarChart, Boxes, Users } from "lucide-react";

export default function Sidebar() {
  return (
    <div className="w-56 bg-black text-white p-4 space-y-6">
      <h1 className="text-xl font-bold">Retail AI</h1>

      <nav className="space-y-4">
        <Link to="/sales" className="flex items-center gap-2 hover:text-gray-300">
          <BarChart size={18} /> Sales
        </Link>

        <Link to="/inventory" className="flex items-center gap-2 hover:text-gray-300">
          <Boxes size={18} /> Inventory
        </Link>

        <Link to="/workforce" className="flex items-center gap-2 hover:text-gray-300">
          <Users size={18} /> Workforce
        </Link>
      </nav>
    </div>
  );
}
