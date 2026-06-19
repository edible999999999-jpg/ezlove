import { BASE_URL } from "./config";

export function uploadImage(tempFilePath) {
  return new Promise((resolve, reject) => {
    const token = uni.getStorageSync("access_token");
    uni.uploadFile({
      url: `${BASE_URL}/upload`,
      filePath: tempFilePath,
      name: "file",
      header: token ? { Authorization: `Bearer ${token}` } : {},
      success: (res) => {
        if (res.statusCode === 200) {
          const data = JSON.parse(res.data);
          resolve(data.url);
        } else {
          reject(new Error("上传失败"));
        }
      },
      fail: (err) => {
        reject(new Error(err?.errMsg || "上传失败"));
      },
    });
  });
}
