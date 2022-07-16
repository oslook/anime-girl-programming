import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import ImageList from '@material-ui/core/ImageList';
import ImageListItem from '@material-ui/core/ImageListItem';
import ImageListItemBar from '@material-ui/core/ImageListItemBar';
import IconButton from '@material-ui/core/IconButton';
import StarBorderIcon from '@material-ui/icons/StarBorder';
import itemData from './itemData';

const useStyles = makeStyles((theme) => ({
  root: {
    display: 'flex',
    flexWrap: 'wrap',
    justifyContent: 'space-around',
    overflow: 'hidden',
    backgroundColor: theme.palette.background.paper,
  },
  imageList: {
    // transform: 'translateZ(0)',
  },
  title: {
    color: theme.palette.primary.contrastText,
  },
  titleBar: {
    background:
      'linear-gradient(to top, rgba(0,0,0,0.7) 0%, rgba(0,0,0,0.3) 70%, rgba(0,0,0,0) 100%)',
  },
}));


export default function TitlebarImageList() {
  const classes = useStyles();

  return (
    <div className={classes.root}>
    <ImageList rowHeight='auto' className={classes.imageList} cols={3.0}>
      {itemData.map((item) => (
        <ImageListItem key={item.img}>
          <img src={item.img} alt={item.title} />
          <ImageListItemBar
            title={item.context.custom.caption}
            subtitle={item.context.custom.author}
            classes={{
              root: classes.titleBar,
              title: classes.title,
            }}
            actionIcon={
              <IconButton aria-label={`star ${item.title}`} href={item.context.custom.original_url}>
                <StarBorderIcon className={classes.title} />
              </IconButton>
            }
          />
        </ImageListItem>
      ))}
    </ImageList>
  </div>
  );
}
