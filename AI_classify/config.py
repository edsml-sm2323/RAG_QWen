local_model_path = "msy"
key = "openai key"
model_name = "gpt-4o-mini"
IPC_num_list = ["A61B5/0476", "A61B5/0478",
                "G05B15/02", "G06K9/66", "G07C9/00", "G08B19/00", "G08B25/10",
                "G05D1/02", "G05D1/08", "G05D1/10", "G05D1/12", "G06F1/16",
                "G06F3/01",
                "G06F9/44", "G06F9/455", "G06N3/00", "G06N3/04", "G06N3/06", "G06N3/063",
                "G06N3/067", "G06N3/10", "G06N3/12", "G06N5/00", "G06N5/02", "G06N5/04",
                "G06K9/00", "G06K9/62", "G06N3/02", "G06N3/08", "G06N7/02", "G06N3/02", "G06N3/08", "G06N99/00", "G06K9/00", "G06N3/02", "G06N7/04", "G06N7/00", "G06N5/02",
                "G06T7/00", "G06K9/00", "G06T1/20", "G06T3/40", "G06T9/00", "G06T-019/20", "G06K9/00", "G06T7/10", "G06T7/215",
                "G06T7/00", "G05B13/02", "G05D1/00", "G06N5/00", "G06F17/28", "G06F17/27", "A61B34/00",
                "B25J9/00", "G10L17/00", "G10L25/00", "G10L99/00", "G10L15/00", "G10L13/00", "G06Q50/26", "G09B", "G06Q50/20",
                "G06Q10/06", "G06Q10/08", "G06Q50/04", "G06Q50/28", "G06F19/24", "G06F19/00", "G16H50/20", "G06F19/10",
                "G06F19/12", "G06F19/14", "G06F19/16", "G06F19/18", "G06F19/20", "G06F19/22", "A61F2/00", "G06F19/24",
                "G06F19/18", "G06N3/12", "G16H", "A61B5", "G16H10/00", "G16H40/00", "G16H50/00", "G16H70/00", "G06Q50/24",
                "G06Q50/26", "G06F21/00", "A61B5/117", "H04W12/00", "H04W12/12", "G06Q40/00", "G08B13/00", "G08B31/00",
                "G06F21/30", "H04W12/06", "H04L9/00", "G06F21/00", "H04L25/03", "H04L25/02", "H04L25/03", "H04N21/466",
                "H04R25/00", "G06F13/00", "H04H", "H04N", "H04M", "H04N7/15", "H04M3/56", "H04M1/253", "B60W30/06", "B60W30/10",
                "B60W30/12", "B60W30/14", "B62D15/02", "B64G1/24", "G06K9/00", "G05D1/00", "F02K", "B60W30/06", "B60W30/10",
                "B60W30/12", "B60W30/14", "B62D15/02", "G05D1/00", "G08G1/017", "G08G1/054", "G08G", "B60W30", "G05B13/02",
                "G05D1/00", "G06E", "G06F9/44", "G06F11/14", "G06F15/00", "G06F17/00", "G06F19/00", "G06J1/00", "G06K7/14",
                "G06K9/00", "G06N", "G06T", "G10L", "G16H50/20", "G01S7/41", "G08B29/18"]

# IPC_num_list = ["A61B5/0476"]


keywords_list = [
        "machine learning", "adaboost", "rankboost", "stochastic gradient descent", "overfitting", "objective function",
    "supervised learning", "training", "cost-sensitive learning", "semi-supervised learning", "unsupervised learning",
    "sequential decision", "apprenticeship learning", "adversarial learning", "multi-task", "transfer learning", "lifelong learning",
    "classification", "regression", "decision tree", "xgboost", "random forest", "support vector machine", "svm",
    "k-nearest neighbors", "instance-based learning", "lazy learning", "active learning", "embedding", "feature selection",
    "regression model", "predictive model", "target function", "test dataset", "training dataset", "validation dataset",
"deep learning", "convolutional network", "recurrent network", "gru", "lstm", "neural network", "multilayer perceptron",
    "backpropagation", "deep blue", "cnn", "rnn", "neural nets", "deep learning", "back propagation", "connectionism", "connectionist",
"natural language processing", "nlp", "text mining", "stemming", "lemmatization", "information extraction", "machine translation",
    "chatbot", "personal assistant", "question answering", "natural language generation", "nlg", "semantics", "semantic analysis",
    "morphology", "morphological analysis", "content extraction", "text analysis", "text recognition", "text analytics", "text analytic",
"computer vision", "visual biometrics", "scene understanding", "activity recognition", "video summarization", "visual indexing",
    "retrieval", "visual inspection", "scene anomaly detection", "camera calibration", "epipolar geometry", "computational photography",
    "hyperspectral imaging", "motion capture", "3d imaging", "active vision", "image representation", "shape representation",
    "texture representations", "object detection", "object recognition", "object tracking", "object matching", "image segmentation",
    "video segmentation", "shape inference", "ar", "vr", "augmented reality", "virtual reality", "facial analysis", "face recognition",
    "reinforcement learning", "stochastic approach", "stochastic technique", "stochastic method",
    "stochastic algorithm",
    "probabilistic approach", "probabilistic reasoning", "reward function", "q-learning", "policy gradient",
    "markov decision processes",
    "actor-critic methods", "apprenticeship learning",
    "data mining", "anomaly detection", "cluster analysis", "clustering", "motif discovery", "dimensionality reduction",
    "manifold learning", "latent representation", "latent variable model", "latent dirichlet allocation",
    "feature selection",
    "embedding", "predictive analytics", "predictive analysis", "predictive purchasing", "predictive analytics",
    "feature engineering",  "expert system", "rule learning", "decision model", "descriptive model", "inductive reasoning", "fuzzy logic",
    "knowledge representation", "knowledge base",  "semantic networks", "entity recognition", "relationship extraction", "SPARQL", "ontology", "knowledge representation",
    "knowledge graph",  "bayesian networks", "probabilistic graphical models", "maximum likelihood model", "maximum entropy model",
    "maximum a posteriori model", "mixture modeling", "conditional random field", "hidden markov model", "generative models",
    "decision support systems", "probabilistic reasoning", "AI ethics", "explainable AI", "XAI", "model interpretability", "autonomous system", "robotics", "autonomous vehicles",
    "driverless", "smart car", "fintech", "cybersecurity", "smart grid", "smart city", "medical imaging",
    "genomic screening", "recommendation systems", "multi-agent system"


]

# keywords_list = [
#         "artificial intelligence", "machine learning", "deep learning", "neural network",
#         "natural language processing"]