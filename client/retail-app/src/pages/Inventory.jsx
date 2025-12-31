import { useState } from "react";
import Layout from "../components/Layout";
import ChartRenderer from "../components/ChartRenderer";
import defaultBlueprint from "../constants/inventoryBlueprint.json";

export default function Inventory() {
  const [blueprint, setBlueprint] = useState(defaultBlueprint);
  const [loading, setLoading] = useState(false);

  return (
    <Layout
      page="inventory"
      setBlueprint={setBlueprint}
      setLoading={setLoading}
      loading={loading}
    >
      <ChartRenderer blueprint={blueprint} loading={loading} />
    </Layout>
  );
}
