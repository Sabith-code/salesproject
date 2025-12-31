import { useState } from "react";
import Layout from "../components/Layout";
import ChartRenderer from "../components/ChartRenderer";
import defaultBlueprint from "../constants/workforceBlueprint.json";

export default function Workforce() {
  const [blueprint, setBlueprint] = useState(defaultBlueprint);
  const [loading, setLoading] = useState(false);

  return (
    <Layout
      page="workforce"
      setBlueprint={setBlueprint}
      setLoading={setLoading}
      loading={loading}
    >
      <ChartRenderer blueprint={blueprint} loading={loading} />
    </Layout>
  );
}
