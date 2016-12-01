from itertools import combinations
import operator

def calculate_rand_index(original_label_dict, predict_label_dict):
    """
    @param original_label_dict: dictionary with keys as document_id and value as label
    @param predict_label_dict: dictionary with keys as document_id and value as label
    """
    tp = 0
    fp = 0
    fn = 0
    tn = 0
    for combo in combinations(predict_label_dict.keys(), 2):
        id1 = combo[0]
        id2 = combo[1]
        if predict_label_dict[id1] == predict_label_dict[id2] and original_label_dict[id1] == original_label_dict[id2]:
            #print (id1,id2),(predict_label_dict[id1],predict_label_dict[id2]), (original_label_dict[id1], original_label_dict[id2])
            tp += 1
        elif predict_label_dict[id1] == predict_label_dict[id2] and original_label_dict[id1] != original_label_dict[id2]:
            fp += 1
        elif predict_label_dict[id1] != predict_label_dict[id2] and original_label_dict[id1] == original_label_dict[id2]:
            fn += 1
        elif predict_label_dict[id1] != predict_label_dict[id2] and original_label_dict[id1] != original_label_dict[id2]:
            tn += 1
    rand_index = (tp + tn)/float((tp + tn + fp + fn))
    precision = ( tp * 1.0 ) / (tp + fp)
    recall =  ( tp * 1.0 ) / (tp + fn)
    jc = ( 1.0 * tp ) / ( tp + fp + fn)
    f1 = 2* ((1.0 * precision*recall)/ (precision+recall))
    purity = calculate_purity(original_label_dict,predict_label_dict)
    #print 'TP : %d\nTN : %d\nFP : %d\nFN : %d\nRand Index : %f\nPrecision : %f\nRecall : %f\nJC : %f\nPurity : %f\n' % (tp, tn, fp, fn, rand_index, precision, recall, jc, purity)
    string = "%d,%d,%d,%d,%f,%f,%f,%f,%f,%f" % (tp, tn, fp, fn, rand_index, precision, recall, f1, jc, purity)
    return string

def calculate_purity(orig_dict, pred_dict):
    """
    @param orig_dict: dictionary with keys as document_id and value as label
    @param pred_dict: dictionary with keys as document_id and value as label
    """
    total = 0
    N = len(pred_dict)
    # get the set of unique cluster ids
    pred_cluster = dict()
    for x in pred_dict:
        if pred_dict[x] in pred_cluster:
            pred_cluster[pred_dict[x]].append(x)
        else:
            pred_cluster[pred_dict[x]]= [x]

    # find out what class is most frequent in each cluster
    for cluster in pred_cluster:
        temp_dict = dict()
        for bid in pred_cluster[cluster]:
            if orig_dict[bid] in temp_dict:
                temp_dict[orig_dict[bid]] += 1
            else:
                temp_dict[orig_dict[bid]] = 1
        total += max(temp_dict.iteritems(), key=operator.itemgetter(1))[1]
        #print total , N
    #print total , N
    return float(total)/ N
