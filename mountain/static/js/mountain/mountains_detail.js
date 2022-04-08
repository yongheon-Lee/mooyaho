const clickedMntInfo = (e) => {
    if (e.target.classList[0] !== 'material-icons') {
        e.target.classList.toggle('text-truncate');
    }
}

const getSpanElement = (text) => {
    const span = document.createElement('span');
    span.textContent = text;
    return span;
}

const m2Km = (meter) => {
    if (meter >= 1000) {
        return `${meter/1000} km`
    } else {
        return `${meter} m`
    }
}

const min2Hour = (min) => {
    if (min >= 60) {
        return `${parseInt(min/60)} 시간 ${min%60} 분`;
    } else {
        return `${min} 분`
    }
}

const displayHikingInfo = (info) => {
    infoArray = [
        `구간거리: ${m2Km(info.property_sec_len)}`,
        `예상 상행시간: ${min2Hour(info.property_up_min)}`,
        `예상 하행시간: ${min2Hour(info.property_down_min)}`,
        `난이도: ${info.property_cat_nam}`
    ];
    
    const hikingInfoArea = document.querySelector('#hiking-info-area');
    infoArray.forEach(eachInfo => {
        hikingInfoArea.appendChild(getSpanElement(eachInfo));
    });
}

const removeHikingInfo = () => {
    const hikingInfoArea = document.querySelector('#hiking-info-area');
    hikingInfoArea.textContent = '';
}

const removeCurrentFeatureOnMap = (curIndex) => {
    hikingMap.data.removeGeoJson(hikingCourseList[curIndex])
    markers.forEach(marker => {
        marker.setMap(null);
    })
    removeHikingInfo();
}

const drawHikingMap = (showIndex, isForward) => {
    if (markers.length > 0) {
        removeCurrentFeatureOnMap(isForward == true ? showIndex-1 : showIndex+1);
    }

    hikingMap.data.addGeoJson(hikingCourseList[showIndex]);
    allFeature = hikingMap.data.getAllFeature()[0]; 
    
    // 등산로 색 변경
    hikingMap.data.setStyle(function(feature){
        const color = 'rgb(200, 154, 121)';

        return {
            fillColor: color,
            strokeColor: color,
            strokeWeight: 6,
            icon: null
        };
    })

    // 등산로 중간점을 센터로
    totalCoordinate = allFeature.geometryCollection[0].coords[0];
    const centerX = totalCoordinate[parseInt(totalCoordinate.length/2)]['y'];
    const centerY = totalCoordinate[parseInt(totalCoordinate.length/2)]['x'];
    hikingMap.setCenter(new naver.maps.LatLng(centerX, centerY))
    
    // 마커 표시
    const markerMessages = ['🔝출발점', '🔚도착점']
    const pointHeight = [allFeature.property_start_z, allFeature.property_end_z]
    for (let i=0; i<markerMessages.length; i++) {
        markers[i] = new naver.maps.Marker({
            position: new naver.maps.LatLng(totalCoordinate[i*(totalCoordinate.length-1)]['y'], totalCoordinate[i*(totalCoordinate.length-1)]['x']),
            map: hikingMap
        })

        let contentString = [
            '<div class="iw_inner">',
            `   <span>${markerMessages[i]}</span><br/>`,
            `   <span>높이:${pointHeight[i]} m</span><br/>`,
            '</div>'
        ].join('');
    
        let infoWindow = new naver.maps.InfoWindow({
            content: contentString
        });
        
        naver.maps.Event.addListener(markers[i], "click", function(e) {
            if (infoWindow.getMap()) {
                infoWindow.close();
            } else {
                infoWindow.open(hikingMap, markers[i]);
            }
        });
    }
    // 등산로 정보 표시
    displayHikingInfo(allFeature);
}

// 등산로 좌, 우 화살표 누르면 ..
const clickedArrow = (e) => {
    const currentHikingCourseIndex = parseInt(document.querySelector('#hiking-area').dataset.index);
    const totalHikingCourseLength = hikingCourseList.length;
    const hikingCourseIndex = document.querySelector('#hiking-course-index');
    let nextHikingCourseIndex = 0;
    let isForward = false;
    
    if (e.target.id === 'f-arrow') {
        if (currentHikingCourseIndex === totalHikingCourseLength-1) {
            alert('마지막 등산코스 입니다');
            return;
        } else {
            nextHikingCourseIndex = currentHikingCourseIndex+1;
            hikingCourseIndex.textContent = nextHikingCourseIndex+1;
            isForward = true;
        }
    } else if (e.target.id === 'b-arrow') {
        if (currentHikingCourseIndex === 0) {
            alert('첫 등산코스 입니다');
            return;
        } else {
            nextHikingCourseIndex = currentHikingCourseIndex-1;
            hikingCourseIndex.textContent = currentHikingCourseIndex;
        }
    } else {
        return;
    }
    drawHikingMap(nextHikingCourseIndex, isForward);
    document.querySelector('#hiking-area').dataset.index = nextHikingCourseIndex.toString();
}

const setHikingMap = () => {
    const coordinate = {
        'maxx': document.querySelector('#hiking-area').dataset.maxx,
        'maxy': document.querySelector('#hiking-area').dataset.maxy,
        'minx': document.querySelector('#hiking-area').dataset.minx,
        'miny': document.querySelector('#hiking-area').dataset.miny
    }
    
    const hikingCourseIndex = parseInt(document.querySelector('#hiking-area').dataset.index);
    const centerX = (parseFloat(coordinate['maxx']) + parseFloat(coordinate['minx'])) / 2
    const centerY = (parseFloat(coordinate['maxy']) + parseFloat(coordinate['miny'])) / 2

    var mapOptions = {
        center: new naver.maps.LatLng(centerY, centerX),
        zoom: 13
    };

    hikingMap = new naver.maps.Map('map', mapOptions);
    naver.maps.Event.once(hikingMap, 'init', function () {
        $.ajax({
            url: `https://api.vworld.kr/req/data?key=63EA231B-2147-3429-8861-ED4408D496F4&request=GetFeature&data=LT_L_FRSTCLIMB&domain=localhost:8000&size=1000&geomFilter=BOX(${coordinate['minx']},${coordinate['miny']},${coordinate['maxx']},${coordinate['maxy']})`,
            dataType: 'jsonp',
            success: startDataLayer
        });
    });

    function startDataLayer(geojson) {
        isHikingResponseOk = true;
        hikingCourseList = geojson.response.result.featureCollection.features;
        drawHikingMap(hikingCourseIndex);
    }
}

const makeInfoCard = (info) => {
    const infoContent = document.querySelector('#restaurant-info-content');
    const contentData = [info.address, info.category];
    let pElement;
    const topDiv = document.createElement('div');
    const secondDiv = document.createElement('div');
    const h5 = document.createElement('h5');
    const aElement = document.createElement('a');

    topDiv.setAttribute('class', 'card');
    secondDiv.setAttribute('class', 'card-body');
    h5.setAttribute('class', 'card-title');
    
    aElement.innerHTML = info.title;
    if (info.link != "") {
        aElement.setAttribute('href', info.link);    
    } else {
        aElement.setAttribute('href', `https://search.naver.com/search.naver?query=${aElement.textContent} ${info.address}`);
    }
    aElement.setAttribute('target', '_blank'); // a태그 클릭 시 새 탭 or 새 윈도우에서 열기 옵션

    h5.appendChild(aElement);
    secondDiv.appendChild(h5);
    contentData.forEach((data, index) => {
        pElement = document.createElement('p');
        pElement.setAttribute('class', 'card-text')
        pElement.innerText = data;
        secondDiv.appendChild(pElement);
    });
    topDiv.appendChild(secondDiv);
    infoContent.appendChild(topDiv);
}

const setNearRestaurantInfo = () => {
    const restaurantInfo = JSON.parse(document.querySelector('#restaurant-info-area').dataset.info);
    if (restaurantInfo.items.length < 1) {
        document.querySelector('#restaurant-info-content').style.textAlign = 'center';
        document.querySelector('#restaurant-info-content').innerHTML = `
            <p>검색 결과가 없습니다</p>
        `;
    }
    restaurantInfo.items.forEach(place => {
        makeInfoCard(place);
    })
}


// 실행부
let hikingCourseList = [];
let hikingMap;
let markers = [];
let isHikingResponseOk = false;
document.querySelector('.mnt-info-area').addEventListener('click', clickedMntInfo);
document.addEventListener("DOMContentLoaded", function() {
    setHikingMap();
    setNearRestaurantInfo();
});

document.querySelectorAll('.arrow-wrapper').forEach(arrowEle => {
    arrowEle.addEventListener('click', clickedArrow);
})

// 등산로 코스 요청에 대한 응답을 받지 못한다면,
$(document).ajaxError(function() {
    document.querySelectorAll('#hiking-area > div').forEach((ele, i) => {
        if (i > 1) ele.parentElement.removeChild(ele);
    })
    document.querySelector('#hiking-course-index').innerHTML = '<span style="color:red">(코스 응답없음)<span>';
})