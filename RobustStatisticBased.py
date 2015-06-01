import skimage.morphology as mor
import numpy as np

test_img = np.array([   [9,   9,  8,   2,   6,  6],
                        [9,   9,  2,  10,   8,  6],
                        [10, 10, 10,  10,  10,  3],
                        [6,   3,  2,  10,   2, 10],
                        [6,   6,  4,   9,  10, 10]  ])

def RobustStatisticBased(img = test_img, zeta = 0.3, L_max = 3,prints = False):
    
    
    new_img = np.zeros_like(img)
    
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            
            for L in range(1, L_max):
                eval = img[max(0,i-L):(min(img.shape[0],i+L)+1),max(0,j-L):(min(img.shape[1],j+L)+1)]
                
                if prints == True:
                    print 'i,j,L = ',i,j,L
                    print 'eval: \n',eval
                
                eval_list = eval#[eval>0]
                if prints == True:
                    print 'eval_list: \n',eval_list
                
                f_ij = img[i][j]
                if prints == True:
                    print 'f_ij:',f_ij
                
                #if len(np.unique(eval_list)) > 0:
                eval_min = np.min(eval_list)
                eval_max = np.max(eval_list)
                eval_med = np.median(eval_list)
                #else:
                 #   eval_min = f_ij
                  #  eval_max = f_ij
                   # eval_med = f_ij
                if prints == True:
                    print 'eval_min: ', eval_min
                    print 'eval_med: ', eval_med
                    print 'eval_max: ', eval_max

                if eval_min < eval_med < eval_max:
                    if eval_min < f_ij < eval_max:
                        if prints == True:
                            print 'f_ij unchanged!'
                        break
                    else:
                        mid = eval_list[eval_list > eval_min]
                        mid = mid[mid < eval_max]
                        if prints == True:
                            print 'mid',mid
                        if np.unique(mid).shape[0] <= 1 and L < L_max:
                            L = L + 1
                            if prints == True:
                                print 'Increasing L to L =',L
                        else:
                            tau = zeta*mid.std()
                            if prints == True:
                                print 'tau:',tau.astype(np.float16)
                            t = tau/np.sqrt(2)
                            if prints == True:
                                print 't:',t
                            x = mid - np.median(eval_list)
                            if prints == True:
                                print 'x:',x
                            mid = (x!=0)*mid
                            mid = mid[mid!=0]
                            if prints == True:
                                print 'mid:',mid
                            x = x[x!=0]
                            if prints == True:
                                print 'x:',x
                            r = 2*x/(t**2+x**2) 
                            if prints == True:
                                print 'r:',r
                            S1 = np.sum(mid*r/x)
                            if prints == True:
                                print 'S1:',S1
                            S2 = np.sum(r/x)
                            if prints == True:
                                print 'S2:',S2
                            f_ij = np.round(S1/S2)
                            if prints == True:
                                print 'long method. f_ij changed to: ',f_ij
                            break
                else:
                    mid = eval_list[eval_list > eval_min]
                    mid = mid[mid < eval_max]
                    if prints == True:
                        print 'mid',mid
                    if np.unique(mid).shape[0] <= 1 and L < L_max:
                        L = L + 1
                        if prints == True:
                            print 'Increasing L to L =',L
                    else:
                        tau = zeta*mid.std()
                        if prints == True:
                            print 'tau:',tau.astype(np.float16)
                        t = tau/np.sqrt(2)
                        if prints == True:
                            print 't:',t
                        x = mid - np.median(eval_list)
                        if prints == True:
                            print 'x:',x
                        mid = (x!=0)*mid
                        mid = mid[mid!=0]
                        if prints == True:
                            print 'mid:',mid
                        x = x[x!=0]
                        if prints == True:
                            print 'x:',x
                        r = 2*x/(t**2+x**2)
                        if prints == True:
                            print 'r:',r
                        S1 = np.sum(mid*r/x)
                        if prints == True:
                            print 'S1:',S1
                        S2 = np.sum(r/x)
                        if prints == True:
                            print 'S2:',S2
                        f_ij = np.round(S1/S2)
                        if prints == True:
                            print 'long method. f_ij changed to: ',f_ij
                        break

            new_img[i][j] = f_ij
            
    new_img = new_img.astype(int)
    if prints == True:
        print 'New image: \n', new_img
    
    if np.array_equal(img,test_img):
        assert (new_img.all() == np.array([    [ 9,  9,  8,  6,  6,  6],
                                               [ 9,  9,  8,  6,  8,  6],
                                               [ 6,  8,  8,  7,  7,  3],
                                               [ 6,  3,  5,  6,  6, 10],
                                               [ 6,  3,  4,  9, 10, 10]   ]).all()), "BROKEN!"
    if prints == True:
        print "Success!"  
    
    return new_img