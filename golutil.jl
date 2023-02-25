using Distributed
using Random
function delta2pos(i,j,di,dj,h,w)
    y=i+di
    x=j+dj
    if y<1
        y=y+h
    elseif y>h
        y=y-h
    end

    if x<1
        x=x+w
    elseif x>w
        x=x-w
    end
    return [y x]
end

@everywhere function calc_nsum(arr,i,j,h,w,r)
    s=0
    @inbounds for dj=-r:r
        @simd for di=-r:r
            loc=delta2pos(i,j,di,dj,h,w)
            s=s+arr[loc[1],loc[2]]
        end
    end
    s=s-arr[i,j]
    return s
end

function calc_alive(state,lnum)
    if state==0 && lnum==3
        return 1
    elseif state==1 && lnum==3
        return 1
    elseif state==1 && lnum==2
        return 1
    else
        return 0
    end
end


function make_rand_life(h,w)
    arr=rand([0,1],h,w)
    return arr
end

function make_zero_arr(h,w)
    arr=zeros(Int64,h,w)
    return arr
end

function step(state,narr,h,w)
    #state_memo=copy(state)
    pmap(j->pmap(i->narr[i,j]=calc_nsum(
        state,i,j,h,w,1
    ),1:h),1:w)
    #narr_memo=copy(narr)
    #pmap((i,j)->narr[i,j]=calc_nsum(state,i,j,h,w,1),1:h,1:w)
    state=calc_alive.(state,narr)
    
    narr=zeros(Int64,h,w)
    return Dict(
        "state"=>state,
        "narr"=>narr
        #"state_memo"=>state_memo,
        #"narr_memo"=>narr_memo
    )
end