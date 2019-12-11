import py4j.GatewayServer;
import info.debatty.java.lsh.LSHSuperBit;
import java.util.Random;
import java.util.Arrays;
import java.util.ArrayList;
import java.util.List;
public class HashApplication {

    public ArrayList<List<Integer>> hash(int stages, int buckets, ArrayList<ArrayList <Double>>vectors) {

        int count = vectors.size();
        int n = vectors.get(0).size();
        LSHSuperBit lsh = new LSHSuperBit(stages, buckets, n);
        ArrayList<List<Integer>> hashes = new ArrayList<>();
        // Compute a SuperBit signature, and a LSH hash
        for (int i = 0; i < count; i++) {
            Double[] vector = (Double[]) vectors.get(i).toArray(new Double[n]);
            double[] vector_u = Arrays.stream(vector).mapToDouble(Double::doubleValue).toArray();

            int[] hash = lsh.hash(vector_u);
            Integer[] hash_b = Arrays.stream(hash).boxed().toArray(Integer[]::new);
            hashes.add(Arrays.asList(hash_b));            
         //    for (double v : vector) {
         //        System.out.printf("%6.2f\t", v);
         //    }
         //    System.out.print(hash[0]);
         //    System.out.print("\n");
         //
        }
        return hashes;
    }

    public static void main(String[] args) {
        HashApplication app = new HashApplication();
        // app is now the gateway.entry_point
        GatewayServer server = new GatewayServer(app);
        server.start();
    }
}


