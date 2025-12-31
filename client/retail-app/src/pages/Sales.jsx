import Layout from "../components/Layout";
import ChartRenderer from "../components/ChartRenderer";
import blueprint from "../constants/salesBlueprint.json";

export default function Sales() {
  return (
    <Layout page="sales">
      <ChartRenderer blueprint={blueprint} />
    </Layout>
  );
}
