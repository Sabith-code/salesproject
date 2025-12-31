import {
    BarChart, Bar, LineChart, Line,
    XAxis, YAxis, Tooltip, ResponsiveContainer
  } from "recharts";
  import { motion, AnimatePresence } from "framer-motion";
  
  export default function ChartRenderer({ blueprint }) {
    return (
      <AnimatePresence mode="wait">
        <motion.div
          key={JSON.stringify(blueprint)}
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0 }}
          className="grid grid-cols-2 gap-6"
        >
          {blueprint.charts.map((chart, i) => (
            <div key={i} className="bg-white p-4 rounded shadow">
              <h3 className="font-semibold mb-2">{chart.title}</h3>
  
              <ResponsiveContainer width="100%" height={250}>
                {chart.type === "bar" && (
                  <BarChart data={chart.data}>
                    <XAxis dataKey="name" />
                    <YAxis />
                    <Tooltip />
                    <Bar dataKey="value" fill="#000" />
                  </BarChart>
                )}
  
                {chart.type === "line" && (
                  <LineChart data={chart.data}>
                    <XAxis dataKey="day" />
                    <YAxis />
                    <Tooltip />
                    <Line dataKey="value" stroke="#000" />
                  </LineChart>
                )}
              </ResponsiveContainer>
            </div>
          ))}
  
          {/* Recommendation */}
          <div className="col-span-2 bg-gray-100 p-4 rounded">
            {blueprint.recommendation}
          </div>
        </motion.div>
      </AnimatePresence>
    );
  }
  