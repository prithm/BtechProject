import mulan.classifier.lazy.MLkNN;
import mulan.classifier.meta.RAkEL;
import mulan.classifier.transformation.LabelPowerset;
import mulan.data.MultiLabelInstances;
import mulan.evaluation.Evaluator;
import mulan.evaluation.MultipleEvaluation;
import weka.classifiers.trees.J48;
import weka.core.Utils;

public class MulanExp1 {

    public static void main(String[] args) throws Exception {
        String arffFilename = Utils.getOption("arff", args); // e.g. -arff emotions.arff
        String xmlFilename = Utils.getOption("xml", args); // e.g. -xml emotions.xml

        MultiLabelInstances dataset = new MultiLabelInstances(arffFilename, xmlFilename);

        RAkEL learner1 = new RAkEL(new LabelPowerset(new J48()));
        MLkNN learner2 = new MLkNN();

        Evaluator eval = new Evaluator();
        MultipleEvaluation results;

        int numFolds = 10;
        results = eval.crossValidate(learner1, dataset, numFolds);
        System.out.println(results);
        results = eval.crossValidate(learner2, dataset, numFolds);
        System.out.println(results);
    }
}
