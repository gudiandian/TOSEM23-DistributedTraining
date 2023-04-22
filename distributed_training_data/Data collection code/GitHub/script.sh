#!/bin/bash

strs=('distributed' 'distribute' 'parallel' 'paralleled' 'parallelism' 'multi-server' 'multi-gpu' 'data-parallel' 'model-parallel' 'dataparallel' 'multi-machine' 'multi_gpu' 'multi-gpus' 'workers')

#collect related issues from horovod repository
current_page=1


max_page=11 #depend on total_count of issues

while (($current_page < $max_page))
do
	curl >horovod-issues-${current_page}.json 'https://api.github.com/search/issues?q=type:issue+repo:horovod/horovod%20-label:bug%20-label:enhancement%20-label:wontfix%20-label:%awaiting%20response%22%20-label:%22update%20docs%22%20+state:closed&sort=created&per_page=100&page='"$current_page"
	python3 preprocess.py horovod-issues-${current_page}.json horovod-issues.txt
	let current_page++
done


#collect related issues from keras repository
current_page=1
index=0
max=13
horovod_max_page=2 #depend on total_count of issues

while(($index<$max))
do
        current_page=1
        while (($current_page < $horovod_max_page))
        do
                curl >keras-issues-${current_page}.json `printf 'https://api.github.com/search/issues?q=%s+in:title%%2Cbody+type:issue+repo:keras-team/keras%%20-label:stale%%20-label:type:feature%%20-label:type:docs%%20-label:%%22type:bug/performance%%22+state:closed&sort=created&per_page=100&page=%d' ${strs[$index]} $current_page`
                python3 preprocess.py keras-issues-${current_page}.json keras-issues.txt
                let current_page++
        done
        let index++
done

curl >keras-issues-${current_page}.json `printf 'https://api.github.com/search/issues?q=multiple gpus+in:title%%2Cbody+type:issue+repo:keras-team/keras%%20-label:stale%%20-label:type:feature%%20-label:type:docs%%20-label:%%22type:bug/performance%%22+state:closed&sort=created&per_page=100&page=1'`
                python3 preprocess.py keras-issues-1.json keras-issues.txt

curl >keras-issues-${current_page}.json `printf 'https://api.github.com/search/issues?q=multiple machines+in:title%%2Cbody+type:issue+repo:keras-team/keras%%20-label:stale%%20-label:type:feature%%20-label:type:docs%%20-label:%%22type:bug/performance%%22+state:closed&sort=created&per_page=100&page=1'`
                python3 preprocess.py keras-issues-1.json keras-issues.txt

curl >keras-issues-${current_page}.json `printf 'https://api.github.com/search/issues?q=multiple servers+in:title%%2Cbody+type:issue+repo:keras-team/keras%%20-label:stale%%20-label:type:feature%%20-label:type:docs%%20-label:%%22type:bug/performance%%22+state:closed&sort=created&per_page=100&page=1'`
                python3 preprocess.py keras-issues-1.json keras-issues.txt

curl >keras-issues-${current_page}.json `printf 'https://api.github.com/search/issues?q=multiple gpu+in:title%%2Cbody+type:issue+repo:keras-team/keras%%20-label:stale%%20-label:type:feature%%20-label:type:docs%%20-label:%%22type:bug/performance%%22+state:closed&sort=created&per_page=100&page=1'`
                python3 preprocess.py keras-issues-1.json keras-issues.txt

curl >keras-issues-${current_page}.json `printf 'https://api.github.com/search/issues?q=multiple machine+in:title%%2Cbody+type:issue+repo:keras-team/keras%%20-label:stale%%20-label:type:feature%%20-label:type:docs%%20-label:%%22type:bug/performance%%22+state:closed&sort=created&per_page=100&page=1'`
                python3 preprocess.py keras-issues-1.json keras-issues.txt

curl >keras-issues-${current_page}.json `printf 'https://api.github.com/search/issues?q=multiple server+in:title%%2Cbody+type:issue+repo:keras-team/keras%%20-label:stale%%20-label:type:feature%%20-label:type:docs%%20-label:%%22type:bug/performance%%22+state:closed&sort=created&per_page=100&page=1'`
                python3 preprocess.py keras-issues-1.json keras-issues.txt



#collect related issues from pytorch repository
#This is the example of label "module:ddp". you ma define your own set of labels
current_page=1
max_page=5 #depend on total_count of issues

while (($current_page < $max_page))
do
	curl >pytorch-issues-${current_page}.json 'https://api.github.com/search/issues?q=type:issue+repo:pytorch/pytorch+label:%22module:%20ddp%22%20-label:enhancement%20-label:feature%20-label:%22function%20request%22+state:closed&sort=created&per_page=100&page='"$current_page"
	python3 preprocess.py pytorch-issues-${current_page}.json pytorch-issues.txt
	let current_page++
done


#collect related issues from tensorflow repository
current_page=1

max_page=30 #depend on total_count of issues

while (($current_page < $max_page))
do
	curl >tensorflow-issues-${current_page}.json 'https://api.github.com/search/issues?q=type:issue+repo:tensorflow/tensorflow%20-label:type:feature%20-label:type:bug%20-label:type:docs-bug%20-label:type:docs-feature%20-label:stalled%20-label:%22stat:awaiting%20response%22%20+label:type:others+state:closed&sort=created&per_page=100&page='"$current_page"
	python3 preprocess.py tensorflow-issues-${current_page}.json tensorflow-issues.txt
	let current_page++
done
