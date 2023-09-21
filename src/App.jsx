import React, { useState, useEffect } from 'react';
import { Table } from 'antd';
import YoutubeEmbed from "./youtube_embed";
import { Col, Row, Card, Spin } from 'antd';
import './App.css';

const App = () => {
  const [videoData, setVideoData] = useState(null);
  const [submitted, setSunmitted] =useState(false);
  const [url, setUrl] = useState('');
  const [comments, setComment] = useState(null);
  const [commentsList, setCommentsList] = useState(null);
  const [wordCloudURL, setWordCloudURL] = useState(null);
  const [pieChartURL, setPieChartURL] = useState(null);
  const [PieChartExtremeURL, setPieChartExtremeURL] = useState(null);
  const [extreme, setExtreme] = useState(null)
  const [eight, setEight] = useState(null)
  const [filteredInfo, setFilteredInfo] = useState({});
  const [sortedInfo, setSortedInfo] = useState({});
//   const [column, setColumn] = useState(null)
  const columns = [
    {
        title: 'コメント',
        dataIndex:  "comment",
        width: "40%",
    },
    {
        title: 'ポジ/ネガ/中立',
        dataIndex: "extremeEmotion",
        width: "20%",
        filters: [
          {
            text: 'Positive',
            value: 'positive',
          },
          {
            text: 'Negative',
            value: 'negative',
          },
          {
            text: 'Neutral',
            value: 'neutral',
          },
        ],
        filteredValue: filteredInfo.extremeEmotion || null,
        onFilter: (value, record) => record.extremeEmotion.includes(value),
        ellipsis: true
    },
    {
      title: '感情分類',
      dataIndex: "eightEmotion",
      width: "15%",
      filters: [
        {
          text: 'Sadness',
          value: 'Sadness',
        },
        {
          text: 'Anticipation',
          value: 'Anticipation',
        },
        {
          text: 'Joy',
          value: 'Joy',
        },
        {
          text: 'Fear',
          value: 'Fear',
        },
        {
          text: 'Surprise',
          value: 'Surprise',
        },
        {
          text: 'Disgust',
          value: 'Disgust',
        },
        {
          text: 'Trust',
          value: 'Trust',
        },
      ],
      filteredValue: filteredInfo.eightEmotion || null,
      onFilter: (value, record) => record.eightEmotion.includes(value),
    },
    {
      title: 'いいね数',
      dataIndex: "likeCount",
      key: "likeCount",
      width: "15%",
      sorter: (a, b) => a.likeCount - b.likeCount,
      sortOrder: sortedInfo.columnKey === 'likeCount' ? sortedInfo.order : null,
      ellipsis: true,
    },
  {
    title: '投稿時間',
    dataIndex: "updatedAt",
    key: "updatedAt",
    width: "25%",
  }
  ];

  const handleChangeTable = (pagination, filters, sorter) => {
    setFilteredInfo(filters);
    setSortedInfo(sorter);
  };
  const handleSubmit = async (e) => {
    e.preventDefault();
    setSunmitted(true)
    setVideoData(null)
    setComment(null)
    setCommentsList(null)
    setEight(null)
    // Send the video URL to the Flask backend
    const response_video = await fetch('http://127.0.0.1:5000/api/video-details', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ url }),
    });

    // Retrieve the video details from the response
    const data = await response_video.json();
    setVideoData(data);

    const response_comment = await fetch('http://127.0.0.1:5000/api/video-comments', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ url }),
    })


    // Retrieve the comment from the response
    const comment_response = await response_comment.json();
    const comment_response_lst = Object.values(comment_response)

    const tmp = []
    comment_response_lst.map(e => tmp.push(e.comment))
    setComment(comment_response_lst);
    setCommentsList(tmp);

    // Emotion eight
    const emotion_dict = new Map([['Joy',0], ['Sadness',0], ['Anticipation',0], ['Surprise',0], ['Anger',0], ['Fear',0], ['Disgust',0], ['Trust', 0]])
    comment_response_lst.map(e => emotion_dict.set(e.eightEmotion, emotion_dict.get(e.eightEmotion)+1))
    const emotion_tmp = []
    for (let [key, value] of emotion_dict) {
      emotion_tmp.push([key, value])
    }
    setEight(emotion_tmp);

    // Emotion extreme
    const extreme_emotion_dict = new Map([["positive",0], ["negative",0], ["neutral",0]]) 
    comment_response_lst.map(e => extreme_emotion_dict.set(e.extremeEmotion, extreme_emotion_dict.get(e.extremeEmotion)+1))
    const extreme_emotion_tmp = []
    for (let [key, value] of extreme_emotion_dict) {
      extreme_emotion_tmp.push([key, value])
    }
    setExtreme(extreme_emotion_tmp);
    
  };

  useEffect(() => {
    const fetchImage = async () => {
      const word_cloud_response = await fetch('http://127.0.0.1:5000/api/video-comments-wordCloud', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ commentsList }),
      });
      const blob = await word_cloud_response.blob();
      const graphUrlCloud = URL.createObjectURL(blob);
      setWordCloudURL(graphUrlCloud);
    }
    fetchImage()
  }, [commentsList])


  useEffect(() => {
    const fetchPieChart = async () => {
          const pieChart_response = await fetch('http://127.0.0.1:5000/api/comments-emotion', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ eight }),
          });
          const blob = await pieChart_response.blob();
          const graphUrlPie = URL.createObjectURL(blob);
          setPieChartURL(graphUrlPie);
        }
    fetchPieChart()
  }, [wordCloudURL])

  useEffect(() => {
    const fetchPieChartExtreme = async () => {
    const pieChart_response_extreme = await fetch('http://127.0.0.1:5000/api/comments-emotion-extreme', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ extreme }),
      });
      const blob = await pieChart_response_extreme.blob();
      const graphUrlPieExtreme = URL.createObjectURL(blob);
      setPieChartExtremeURL(graphUrlPieExtreme);
    }
    fetchPieChartExtreme()
  }, [pieChartURL])



  return (
    
    <div>
    <form onSubmit={handleSubmit}>
          <input type="text" value={url} size="45" onChange={(e) => setUrl(e.target.value)} />
          <button type="submit">動画を検索</button>
      </form>
    {submitted && !(videoData && comments && commentsList && eight) && 
    <div className="centered"> 
    <Spin tip="Loading" size="large">
        <div className="content" />
      </Spin>
    </div>
      }
    
    {videoData && comments && commentsList && eight && (
      <>
        <Row type="flex">  
          <Col xs={10}>
          <Card style={{
            height: 400,
          }}>
          <h2>{videoData.title}</h2>
          <Row>
          <Col xs={15}>
          {videoData.videoId && <YoutubeEmbed embedId={videoData.videoId} />}
          </Col>
          <Col xs={6}>
           <li>視聴回数　: {videoData.viewCount}</li>
           <li>いいね数　: {videoData.likeCount}</li>
           <li>コメント数: {videoData.commentCount}</li>
          </Col>
          </Row>
           </Card>
          </Col>
          <Col xs={7}>
          <Card style={{
            height: 400,
          }}>
          {pieChartURL && <img src={pieChartURL} alt="Pie Chart" width="350" height="350"/>}
          </Card>
          </Col>
          <Col xs={7}>
          <Card style={{
            height: 400,
          }}>
          {PieChartExtremeURL && <img src={PieChartExtremeURL} alt="Pie Chart" width="350" height="350"/>}
          </Card>
          </Col>
      </Row>
      <Row type="flex"> 
      <Col xs={15}>
      <Card style={{
            height: 450,
          }}>
      <Table
          columns={columns}
          dataSource={comments}
          onChange={handleChangeTable}
          scroll={{
            y: 280,
          }}
      />
      </Card>
      </Col>
      <Col xs={9}>
      <Card style={{
            height: 450,
          }}>
      {wordCloudURL && <img src={wordCloudURL} alt="Word Cloud" width="500" height="400"/>}
      </Card>
      </Col>
      </Row>
      </>
    )}
    </div>
  );
};

export default App;


