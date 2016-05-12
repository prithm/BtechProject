import java.io.FileWriter;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;


import java.io.InputStream;
import java.io.Reader;
import java.io.StringReader;
import java.util.Iterator;
import java.util.LinkedList;
import java.util.List;
import java.util.ArrayList;

import edu.udo.cs.wvtool.config.WVTConfiguration;
import edu.udo.cs.wvtool.config.WVTConfigurationFact;
import edu.udo.cs.wvtool.config.WVTConfigurationRule;
import edu.udo.cs.wvtool.generic.output.WordVectorWriter;
import edu.udo.cs.wvtool.generic.stemmer.DummyStemmer;
import edu.udo.cs.wvtool.generic.stemmer.LovinsStemmerWrapper;
import edu.udo.cs.wvtool.generic.stemmer.PorterStemmerWrapper;
import edu.udo.cs.wvtool.generic.stemmer.WVTStemmer;
import edu.udo.cs.wvtool.generic.vectorcreation.TermFrequency;
import edu.udo.cs.wvtool.generic.vectorcreation.TFIDF;
import edu.udo.cs.wvtool.main.WVTDocumentInfo;
import edu.udo.cs.wvtool.main.WVTFileInputList;
import edu.udo.cs.wvtool.main.WVTWordVector;
import edu.udo.cs.wvtool.main.WVTool;
import edu.udo.cs.wvtool.wordlist.WVTWordList;

import edu.udo.cs.wvtool.generic.charmapper.WVTCharConverter;
import edu.udo.cs.wvtool.generic.inputfilter.WVTInputFilter;
import edu.udo.cs.wvtool.generic.loader.WVTDocumentLoader;
import edu.udo.cs.wvtool.generic.output.WVTOutputFilter;
import edu.udo.cs.wvtool.generic.stemmer.WVTStemmer;
import edu.udo.cs.wvtool.generic.tokenizer.WVTTokenizer;
import edu.udo.cs.wvtool.generic.vectorcreation.WVTVectorCreator;
import edu.udo.cs.wvtool.generic.wordfilter.WVTWordFilter;
import edu.udo.cs.wvtool.util.TokenEnumeration;
import edu.udo.cs.wvtool.util.WVToolException;
import edu.udo.cs.wvtool.util.WVToolLogger;
import edu.udo.cs.wvtool.main.WVTInputList;

/**
 * An example program on how to use the word vector tool.
 * 
 * @author Michael Wurst
 * @version $Id$
 * 
 */
public class WVToolExample {
	
     /**
     * Returns tokens from an input list.
     * 
     * @param input the input list
     * @param config the configuration
     * @param wordList a word list (possibly containing document and class frequencies).
     * @throws Exception
     */
    public static List<String> prithTokens(WVTInputList input, WVTConfiguration config, WVTWordList wordList) throws WVToolException {

        // Set up the word list properly

        wordList.setAppendWords(false);
        wordList.setUpdateOnlyCurrent(true);

        // Initialize pointers to components for the individual steps
        WVTDocumentLoader loader = null;
        WVTInputFilter infilter = null;
        WVTCharConverter charConverter = null;
        WVTTokenizer tokenizer = null;
        WVTWordFilter wordFilter = null;
        WVTStemmer stemmer = null;
        WVTVectorCreator vectorCreator = null;
        WVTOutputFilter outputFilter = null;
	List<String> overallTokens = new ArrayList<String>();

        // Obtain an expanded list of all documents to consider
        Iterator inList = input.getEntries();
	
	boolean skipErrors = false;

        // Get through the list
        while (inList.hasNext()) {

            WVTDocumentInfo d = (WVTDocumentInfo) inList.next();

            try {

                // Intialize all required components for this document

                loader = (WVTDocumentLoader) config.getComponentForStep(WVTConfiguration.STEP_LOADER, d);
                infilter = (WVTInputFilter) config.getComponentForStep(WVTConfiguration.STEP_INPUT_FILTER, d);
                charConverter = (WVTCharConverter) config.getComponentForStep(WVTConfiguration.STEP_CHAR_MAPPER, d);
                tokenizer = (WVTTokenizer) config.getComponentForStep(WVTConfiguration.STEP_TOKENIZER, d);
                wordFilter = (WVTWordFilter) config.getComponentForStep(WVTConfiguration.STEP_WORDFILTER, d);
                stemmer = (WVTStemmer) config.getComponentForStep(WVTConfiguration.STEP_STEMMER, d);

                //vectorCreator = (WVTVectorCreator) config.getComponentForStep(WVTConfiguration.STEP_VECTOR_CREATION, d);

                //outputFilter = (WVTOutputFilter) config.getComponentForStep(WVTConfiguration.STEP_OUTPUT, d);

                // Process the document

                TokenEnumeration tokens = stemmer.stem(wordFilter.filter(tokenizer.tokenize(charConverter.convertChars(infilter.convertToPlainText(loader.loadDocument(d), d), d), d), d), d);
		String curTokens = new String(" ");
                while (tokens.hasMoreTokens()) {
                    curTokens = curTokens.concat(" " + tokens.nextToken());
                }
		overallTokens.add(curTokens);

                //outputFilter.write(vectorCreator.createVector(wordList.getFrequenciesForCurrentDocument(), wordList.getTermCountForCurrentDocument(), wordList, d));

                wordList.closeDocument(d);
                loader.close(d);

            } catch (WVToolException e) {

                // If an error occurs add it to the error log
                WVToolLogger.getGlobalLogger().logException("Problems processing document " + d.getSourceName(), e);

                // close the input stream for this document
                loader.close(d);

                // If errors should not be skip throw an exception
                if (!skipErrors)
                    throw new WVToolException("Problems processing document " + d.getSourceName(), e);

                // otherwise do nothing and proceed with the next document

            }

        }
	return overallTokens;

    }



    public static void main(String[] args) throws Exception {

        // EXAMPLE HOW TO CALL THE PROGRAM FROM JAVA

        // Initialize the WVTool
        WVTool wvt = new WVTool(false);

        // Initialize the configuration
        WVTConfiguration config = new WVTConfiguration();

        final WVTStemmer dummyStemmer = new DummyStemmer();
        final WVTStemmer porterStemmer = new PorterStemmerWrapper();

        config.setConfigurationRule(WVTConfiguration.STEP_STEMMER, new WVTConfigurationRule() {
            public Object getMatchingComponent(WVTDocumentInfo d) {

                if (d.getContentLanguage().equals("english"))
                    return porterStemmer;
                else
                    return dummyStemmer;
            }
        });

        WVTStemmer stemmer = new LovinsStemmerWrapper();

        config.setConfigurationRule(WVTConfiguration.STEP_STEMMER, new WVTConfigurationFact(stemmer));

        // Initialize the input list with two classes
        WVTFileInputList list = new WVTFileInputList(1);

        // Add entries
        //list.addEntry(new WVTDocumentInfo("../data/alt.atheism", "txt", "", "german", 0));
        //list.addEntry(new WVTDocumentInfo("../data/soc.religion.christian", "txt", "", "english", 0));
	list.addEntry(new WVTDocumentInfo("../../../EnTagRecData", "txt", "utf-8", "english", 0));
        
	// Generate the word list

        WVTWordList wordList = wvt.createWordList(list, config);

        // Prune the word list

        wordList.pruneByFrequency(20, 200000000);

        // Alternativ I: read an already created word list from a file
        // WVTWordList wordList2 =
        // new WVTWordList(new FileReader("/home/wurst/tmp/wordlisttest.txt"));

        // Alternative II: Use predifined dimensions
        // List dimensions = new Vector();
        // dimensions.add("atheist");
        // dimensions.add("christian");
        // wordList =
        // wvt.createWordList(list, config, dimensions, false);

        // Store the word list in a file
        wordList.storePlain(new FileWriter("wordlist.txt"));
	System.out.println(wordList.getNumDocuments());
        // Create the word vectors

        // Set up an output filter (write sparse vectors to a file)
        FileWriter outFile = new FileWriter("wv_tfidf.txt");
        WordVectorWriter wvw = new WordVectorWriter(outFile, true);

        config.setConfigurationRule(WVTConfiguration.STEP_OUTPUT, new WVTConfigurationFact(wvw));

        config.setConfigurationRule(WVTConfiguration.STEP_VECTOR_CREATION, new WVTConfigurationFact(new TFIDF()));
	//config.setConfigurationRule(WVTConfiguration.STEP_VECTOR_CREATION, new WVTConfigurationFact(new TermFrequency()));
        
	// Create the vectors
        wvt.createVectors(list, config, wordList);

        // Alternatively: create word list and vectors together
        // wvt.createVectors(list, config);

        // Close the output file
        wvw.close();
        outFile.close();
	List<String> overallTokens = prithTokens(list, config, wordList);	
	System.out.println(overallTokens.size());	
	BufferedWriter myOutput = null;
        try {
            File file = new File("tokenized.txt");
            myOutput = new BufferedWriter(new FileWriter(file));
            for (String temp : overallTokens){
		myOutput.write(temp+'\n');
	    }
	    myOutput.close();
        } catch ( IOException e ) {
            e.printStackTrace();
        }
	
        // Just for demonstration: Create a vector from a String
        //WVTWordVector q = wvt.createVector("cmu harvard net", wordList);
	//System.out.println(q);
    }

}
