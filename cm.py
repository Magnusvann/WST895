import skimage.measure as meas
import skimage.morphology as mor
import numpy as np
from scipy.stats import itemfreq
 
test_img = np.array([[9,   9,  8,  2,  6,   6],
                    [9,   9,  2, 10,  8,   6],
                    [10, 10, 10, 10, 10,   3],
                    [6,   3,  2, 10,  2,  10],
                    [6,   6,  4,  9, 10,  10]])

def p_list(connpnts,p):
    list = []
    freq = itemfreq(connpnts)
    for i in range(freq.shape[0]):
        if freq[i][1] == p:
           list.append(i)
    return list

def ConnectedMedian(img = test_img ,p_max=15, n_max=5,connectivity=4, prints = False, Test = False):
    
    if img.shape[0]*img.shape[1] > 100:
        prints = False
        
    ori_img = img.copy()
    
    for p in range(1,p_max+1):
        if prints == True:
            print "For p =",p,"\n"
        connpnts = meas.label(img, neighbors=connectivity)
        if prints == True:
            print "Connected sets: \n",connpnts,"\n"
        connpnts_list = p_list(connpnts,p)
        if prints == True:
            print "Connected set having p connected pixels: \n",connpnts_list,"\n"
        
        new_img = np.ones_like(img)*999
        
        for i in connpnts_list: 
            if prints == True:
                print "For connected set ",i,":\n"
            conn_comp_bin = (connpnts == i)
            if prints == True:
                print "Binary mask for connected set: \n",conn_comp_bin,"\n"
            conn_comp_img = conn_comp_bin*img
            if prints == True:
                print "Connected set in image: \n",conn_comp_img,"\n"
            
            for n in range(1,n_max+1):

                bindil = mor.binary_dilation(conn_comp_bin, mor.disk(n))
                if prints == True:
                    print "Binary dilated mask for connected set: \n",bindil,"\n"

                a_list = img[bindil==1]
                if prints == True:
                    print "List of pixel values considered: \n",a_list,"\n"

                f_ij = np.max(conn_comp_img)
                if prints == True:
                    print "f_ij = ",f_ij

                K_min = np.min(a_list)
                if prints == True:
                    print "K_min = ",K_min
                K_med = np.median(a_list)
                if prints == True:
                    print "K_med = ",K_med
                K_max = np.max(a_list)
                if prints == True:
                    print "K_max = ",K_max,"\n"

                if K_min < K_med < K_max:
                    if f_ij == K_max or f_ij == K_min:
                        new_f_ij = K_med
                        conn_comp_img = (conn_comp_bin==1)*new_f_ij
                        if prints == True:
                            print "New f_ij is the median","\n"
                    else:
                        if prints == True:
                            print "Signal! No new value for f_ij needed.","\n"
                    break
                elif n == n_max:
                    new_f_ij = K_med
                    conn_comp_img = (conn_comp_bin==1)*new_f_ij
                    if prints == True:
                        print "New f_ij is the median","\n"
    
            new_img = new_img - conn_comp_bin*999 + conn_comp_img
            if prints == True:
                print "New image after connected set",i,"was processed.\n",new_img,"\n"
        
        img = new_img*(new_img!=999) + img*(new_img==999)
        img = img.astype(int)
        if prints == True:
            print "New image after p =",p,"was processed.","\n",img
            
    if np.array_equal(ori_img,test_img):
        assert (img == np.array(  [[9, 9, 8, 7, 6, 6],
                                   [9, 9, 9, 9, 8, 6],
                                   [9, 9, 9, 9, 9, 8],
                                   [6, 3, 4, 9, 8, 9],
                                   [6, 6, 4, 9, 9, 9]])).all(), "BROKEN!"
    if Test == True:
        print "Success!"
 

    return img