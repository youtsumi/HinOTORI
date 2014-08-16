module HinOTORI {
	exception Error {
		string reason;
	};

	interface Camera { 
		["amd"] void Take( double expt, string filename, bool shutter )
			throws Error;
		double GetTemperature(  );
		void SetTemperature(  );
	};

	interface Telescope { 
		double GetFocusZ(  );
		void SetFocusZ( double z );
		void OpenMirror(  );
		void CloseMirror(  );
	};

	interface Mount { 
		double GetRa(  );
		double GetDec(  );
	};

};
