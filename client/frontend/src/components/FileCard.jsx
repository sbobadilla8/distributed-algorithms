import { useEffect, useState } from "react";
import axios from "axios";
import {
  Box,
  Heading,
  IconButton,
  Progress,
  Stat,
  StatGroup,
  StatLabel,
  StatNumber,
  useToast,
} from "@chakra-ui/react";
import { BsDownload } from "react-icons/bs";
import { humanFileSize } from "../utils/fileSize.js";

const FileCard = ({ item, setResults, backendAddress }) => {
  const toast = useToast();

  const [isDownloading, setIsDownloading] = useState(false);
  const startDownload = async (item) => {
    try {
      await axios.post(`http://${backendAddress}/download`, {
        filename: item.filename,
        size: item.size,
        clients: item.clients,
        checksum: item.checksum,
      });
      setIsDownloading(true);
    } catch (e) {
      toast({
        title: "Error",
        description: "Something went wrong.",
        status: "error",
        duration: 3000,
        isClosable: true,
      });
    }
  };

  useEffect(() => {
    let intervalId;
    if (isDownloading) {
      intervalId = setInterval(async () => {
        const { data } = await axios.get(
          `http://${backendAddress}/download?filename=${item.filename}`
        );
        const progress = parseFloat(data.value);
        setResults((prev) => {
          let temp = [...prev];
          const file = temp.find(
            (tempItem) => tempItem.filename === item.filename
          );
          file.progress = progress;
          return temp;
        });
        if (progress === 1.0) {
          setIsDownloading(false);
        }
      }, 1000);
    }
    return () => clearInterval(intervalId);
  }, [isDownloading, item.progress]);

  return (
    <Box key={`result-${item.filename}`}>
      <Heading size="md" textTransform="uppercase">
        {item.filename}
      </Heading>
      <StatGroup>
        <Stat>
          <StatLabel>Clients sharing</StatLabel>
          <StatNumber>{item.clients.length}</StatNumber>
        </Stat>
        <Stat>
          <StatLabel>Size</StatLabel>
          <StatNumber>{humanFileSize(item.size)}</StatNumber>
        </Stat>
        <Stat>
          <StatLabel>Number of blocks</StatLabel>
          <StatNumber>{item.blocks}</StatNumber>
        </Stat>
        <IconButton
          aria-label="download"
          colorScheme="teal"
          size="lg"
          onClick={() => startDownload(item)}
          icon={<BsDownload />}
        />
      </StatGroup>
      <Progress value={item.progress * 100} />
    </Box>
  );
};
export default FileCard;
